#!/usr/bin/env python3
"""Build a Graphify graph for this RGBDS disassembly.

Stock graphify does not classify `.asm` files as code. This script keeps the
Graphify output format and analysis pipeline, but feeds it a deterministic
RGBDS extraction built from labels, SECTIONs, INCLUDEs, INCBINs, and common
call/reference forms.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.detect import save_manifest
from graphify.export import to_json
from graphify.ids import make_id
from graphify.report import generate
from graphify.wiki import to_wiki


ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
OUT = ROOT / "graphify-out"

NOISE_DIRS = {
    ".git",
    "graphify-out",
}

ASM_EXTS = {".asm", ".inc"}
ROOT_CODE_FILES = {
    "Makefile",
    "layout.link",
    ".rgbds-version",
}
DOC_EXTS = {".md", ".yml", ".yaml"}
TOOL_EXTS = {".c", ".h", ".py", ".sh"}

INCLUDE_RE = re.compile(r'\bINCLUDE\s+"([^"]+)"', re.IGNORECASE)
INCBIN_RE = re.compile(r'\bINCBIN\s+"([^"]+)"', re.IGNORECASE)
SECTION_RE = re.compile(r'^\s*SECTION\s+"([^"]+)"\s*,\s*([A-Za-z0-9_$]+)', re.IGNORECASE)
LABEL_RE = re.compile(r"^\s*([A-Za-z_.$][A-Za-z0-9_.$@{}]*)::?\s*(?=[:\s;]|$)")
MACRO_RE = re.compile(r"^\s*([A-Za-z_.$][A-Za-z0-9_.$@{}]*)\s+MACRO\b", re.IGNORECASE)
CALL_RE = re.compile(r"\b(call|jp|jr|rst)\s+([^;\n]+)", re.IGNORECASE)
MACRO_CALL_RE = re.compile(r"\b(farcall|predef|callba|callab|homecall)\s+([A-Za-z_.$][A-Za-z0-9_.$@]*)", re.IGNORECASE)
LD_PTR_RE = re.compile(r"\bld\s+(hl|de|bc),\s*([A-Za-z_.$][A-Za-z0-9_.$@]*)", re.IGNORECASE)
DATA_REF_RE = re.compile(r"\b(dw|dba|dbw|dab|addr|bank)\s+([^;\n]+)", re.IGNORECASE)
TOKEN_RE = re.compile(r"\b[A-Za-z_.$][A-Za-z0-9_.$@]*\b")

CONDITIONS = {"z", "nz", "c", "nc"}
DIRECTIVES = {
    "SECTION",
    "INCLUDE",
    "INCBIN",
    "IF",
    "ELSE",
    "ELIF",
    "ENDC",
    "MACRO",
    "ENDM",
    "REPT",
    "ENDR",
    "FOR",
    "UNION",
    "NEXTU",
    "ENDU",
    "ASSERT",
    "PURGE",
    "PRINTT",
    "PRINTV",
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def strip_comment(line: str) -> str:
    return line.split(";", 1)[0].rstrip()


def supported_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            parts = path.relative_to(ROOT).parts
        except ValueError:
            continue
        if any(part in NOISE_DIRS for part in parts):
            continue
        if path.suffix.lower() in ASM_EXTS:
            files.append(path)
        elif path.name in ROOT_CODE_FILES:
            files.append(path)
        elif path.suffix.lower() in TOOL_EXTS and parts[:1] == ("tools",):
            files.append(path)
        elif path.suffix.lower() in DOC_EXTS and (len(parts) == 1 or parts[0] in {".github"}):
            files.append(path)
    return sorted(files, key=lambda p: rel(p))


class GraphBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.edges: dict[tuple[str, str, str, str | None], dict] = {}
        self.label_defs: dict[str, str] = {}
        self.file_labels: dict[str, list[str]] = defaultdict(list)
        self.file_sections: dict[str, list[tuple[int, str]]] = defaultdict(list)
        self.files = supported_files()

    def node(
        self,
        node_id: str,
        label: str,
        node_type: str,
        *,
        file_type: str = "code",
        source_file: str = "",
        line: int | None = None,
    ) -> str:
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "label": label,
                "type": node_type,
                "file_type": file_type,
                "source_file": source_file,
            }
            if line is not None:
                self.nodes[node_id]["source_location"] = f"L{line}"
        return node_id

    def edge(
        self,
        source: str,
        target: str,
        relation: str,
        *,
        source_file: str = "",
        line: int | None = None,
        confidence: str = "EXTRACTED",
    ) -> None:
        key = (source, target, relation, f"{source_file}:{line}" if line else None)
        if key in self.edges:
            return
        data = {
            "source": source,
            "target": target,
            "relation": relation,
            "confidence": confidence,
            "source_file": source_file,
            "weight": 1.0 if confidence == "EXTRACTED" else 0.5,
        }
        if line is not None:
            data["source_location"] = f"L{line}"
        self.edges[key] = data

    def file_node(self, path: Path) -> str:
        r = rel(path)
        ftype = "document" if path.suffix.lower() in DOC_EXTS else "code"
        return self.node(make_id("file", r), r, "file", file_type=ftype, source_file=r, line=1)

    def domain_node(self, path: Path) -> str | None:
        r = rel(path)
        parts = Path(r).parts
        if len(parts) == 1:
            domain = "(root)"
        elif parts[0] == "engine" and len(parts) > 2:
            domain = "/".join(parts[:2])
        elif parts[0] in {"data", "audio", "gfx"} and len(parts) > 2:
            domain = "/".join(parts[:2])
        else:
            domain = parts[0]
        node_id = make_id("domain", domain)
        return self.node(node_id, domain, "domain", file_type="concept")

    def first_pass(self) -> None:
        project = self.node(make_id("project", ROOT.name), ROOT.name, "project", file_type="concept")
        for path in self.files:
            r = rel(path)
            file_id = self.file_node(path)
            domain_id = self.domain_node(path)
            if domain_id:
                self.edge(project, domain_id, "contains", source_file=r)
                self.edge(domain_id, file_id, "contains", source_file=r)

            current_section: str | None = None
            for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                line = strip_comment(raw)
                section = SECTION_RE.search(line)
                if section:
                    name, bank = section.groups()
                    section_id = self.node(
                        make_id(r, "section", name),
                        f'{name} [{bank}]',
                        "section",
                        source_file=r,
                        line=line_no,
                    )
                    bank_id = self.node(make_id("bank", bank), bank, "bank", file_type="concept")
                    self.edge(file_id, section_id, "contains", source_file=r, line=line_no)
                    self.edge(section_id, bank_id, "declares_in", source_file=r, line=line_no)
                    current_section = section_id
                    self.file_sections[r].append((line_no, section_id))
                    continue

                macro = MACRO_RE.search(line)
                if macro:
                    name = macro.group(1)
                    if self.valid_label(name):
                        node_id = self.node(make_id(r, "macro", name), name, "macro", source_file=r, line=line_no)
                        self.label_defs.setdefault(name, node_id)
                        self.file_labels[r].append(node_id)
                        self.edge(file_id, node_id, "defines", source_file=r, line=line_no)
                    continue

                label = self.extract_label(line)
                if label:
                    node_id = self.node(make_id(r, "label", label), label, "label", source_file=r, line=line_no)
                    self.label_defs.setdefault(label, node_id)
                    self.file_labels[r].append(node_id)
                    self.edge(file_id, node_id, "defines", source_file=r, line=line_no)
                    if current_section:
                        self.edge(current_section, node_id, "contains", source_file=r, line=line_no)

    def second_pass(self) -> None:
        for path in self.files:
            r = rel(path)
            file_id = self.file_node(path)
            current_label = file_id
            current_section: str | None = None
            section_iter = iter(sorted(self.file_sections.get(r, [])))
            next_section = next(section_iter, None)

            for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                while next_section and line_no >= next_section[0]:
                    current_section = next_section[1]
                    next_section = next(section_iter, None)

                line = strip_comment(raw)
                label = self.extract_label(line)
                if label and label in self.label_defs:
                    current_label = self.label_defs[label]

                for target in INCLUDE_RE.findall(line):
                    target_id = self.ensure_path_node(target, source_file=r, line=line_no)
                    self.edge(file_id, target_id, "imports", source_file=r, line=line_no)

                for target in INCBIN_RE.findall(line):
                    target_id = self.ensure_path_node(target, source_file=r, line=line_no, asset=True)
                    self.edge(current_label, target_id, "embeds", source_file=r, line=line_no)
                    if current_section:
                        self.edge(current_section, target_id, "contains", source_file=r, line=line_no)

                for target in self.call_targets(line):
                    self.reference(current_label, target, "calls", r, line_no)

                for target in self.pointer_targets(line):
                    self.reference(current_label, target, "references", r, line_no)

    def ensure_path_node(self, target: str, *, source_file: str, line: int, asset: bool = False) -> str:
        target_path = (ROOT / target).resolve()
        try:
            target_rel = target_path.relative_to(ROOT).as_posix()
        except ValueError:
            target_rel = target
        file_type = "image" if asset else ("document" if Path(target_rel).suffix.lower() in DOC_EXTS else "code")
        node_type = "asset" if asset else "file"
        return self.node(
            make_id("file", target_rel),
            target_rel,
            node_type,
            file_type=file_type,
            source_file=target_rel if (ROOT / target_rel).exists() else source_file,
            line=1 if (ROOT / target_rel).exists() else line,
        )

    def reference(self, source_id: str, target: str, relation: str, source_file: str, line: int) -> None:
        target = target.strip()
        if not target or target.startswith("$") or target.startswith("%"):
            return
        if target in CONDITIONS or target.upper() in DIRECTIVES:
            return
        target_id = self.label_defs.get(target)
        if not target_id:
            return
        if source_id == target_id:
            return
        self.edge(source_id, target_id, relation, source_file=source_file, line=line)

    @staticmethod
    def valid_label(label: str) -> bool:
        if "{" in label or "}" in label:
            return False
        if label.startswith("."):
            return False
        if label.upper() in DIRECTIVES:
            return False
        return True

    def extract_label(self, line: str) -> str | None:
        match = LABEL_RE.search(line)
        if not match:
            return None
        label = match.group(1)
        return label if self.valid_label(label) else None

    def call_targets(self, line: str) -> list[str]:
        targets: list[str] = [m.group(2) for m in MACRO_CALL_RE.finditer(line)]
        for match in CALL_RE.finditer(line):
            raw = match.group(2).strip()
            parts = [p.strip() for p in raw.split(",")]
            candidate = parts[1] if parts and parts[0].lower() in CONDITIONS and len(parts) > 1 else parts[0]
            token = TOKEN_RE.search(candidate)
            if token:
                targets.append(token.group(0))
        return targets

    def pointer_targets(self, line: str) -> list[str]:
        targets = [m.group(2) for m in LD_PTR_RE.finditer(line)]
        for match in DATA_REF_RE.finditer(line):
            for token in TOKEN_RE.findall(match.group(2)):
                targets.append(token)
        return targets

    def extraction(self) -> dict:
        return {
            "nodes": list(self.nodes.values()),
            "edges": list(self.edges.values()),
            "hyperedges": [],
            "input_tokens": 0,
            "output_tokens": 0,
        }


def word_count(files: list[Path]) -> int:
    total = 0
    for path in files:
        total += len(TOKEN_RE.findall(path.read_text(encoding="utf-8", errors="ignore")))
    return total


def detection(files: list[Path]) -> dict:
    by_type: dict[str, list[str]] = {"code": [], "document": [], "paper": [], "image": [], "video": []}
    for path in files:
        r = rel(path)
        if path.suffix.lower() in DOC_EXTS:
            by_type["document"].append(r)
        else:
            by_type["code"].append(r)
    for values in by_type.values():
        values.sort()
    return {
        "files": by_type,
        "total_files": sum(len(v) for v in by_type.values()),
        "total_words": word_count(files),
        "needs_graph": True,
        "warning": (
            "Custom RGBDS extraction: stock graphify does not classify .asm; "
            "this graph was generated by tools/graphify_rgbds.py and then "
            "built/analyzed with Graphify."
        ),
        "skipped_sensitive": [],
        "unclassified": [],
        "graphifyignore_patterns": 0,
        "scan_root": str(ROOT),
    }


def community_label(G, nodes: list[str]) -> str:
    sources = [G.nodes[n].get("source_file", "") for n in nodes]
    dirs: Counter[str] = Counter()
    banks: Counter[str] = Counter()
    types: Counter[str] = Counter()
    for src in sources:
        parts = Path(src).parts if src else ()
        if not parts:
            continue
        if parts[0] == "engine" and len(parts) > 1:
            dirs[f"engine/{parts[1]}"] += 1
        elif parts[0] in {"data", "audio", "gfx"} and len(parts) > 1:
            dirs[f"{parts[0]}/{parts[1]}"] += 1
        else:
            dirs[parts[0]] += 1
    for n in nodes:
        d = G.nodes[n]
        types[d.get("type", "node")] += 1
        if d.get("type") == "bank":
            banks[d.get("label", "")] += 1
    if banks:
        return f"Bank {banks.most_common(1)[0][0]}"
    if dirs:
        name = dirs.most_common(1)[0][0]
        return name.replace("_", " ").replace("/", " ").title()
    if types:
        return types.most_common(1)[0][0].replace("_", " ").title()
    return "RGBDS Graph"


def unique_labels(labels: dict[int, str]) -> dict[int, str]:
    seen: Counter[str] = Counter()
    out: dict[int, str] = {}
    for cid in sorted(labels):
        label = labels[cid]
        seen[label] += 1
        out[cid] = label if seen[label] == 1 else f"{label} {seen[label]}"
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".graphify_root").write_text(str(ROOT), encoding="utf-8")

    builder = GraphBuilder()
    builder.first_pass()
    builder.second_pass()

    extract = builder.extraction()
    detect = detection(builder.files)
    (OUT / ".graphify_detect.json").write_text(json.dumps(detect, indent=2), encoding="utf-8")
    (OUT / ".graphify_extract.json").write_text(json.dumps(extract, indent=2), encoding="utf-8")

    G = build_from_json(extract, root=str(ROOT), directed=True)
    if G.number_of_nodes() == 0:
        raise SystemExit("ERROR: Graph is empty")

    communities = cluster(G)
    cohesion = score_all(G, communities)
    labels = unique_labels({cid: community_label(G, nodes) for cid, nodes in communities.items()})
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)

    wrote = to_json(G, communities, str(OUT / "graph.json"), force=True, community_labels=labels)
    if not wrote:
        raise SystemExit("ERROR: graphify refused to write graph.json")

    report = generate(
        G,
        communities,
        cohesion,
        labels,
        gods,
        surprises,
        detect,
        {"input": 0, "output": 0},
        str(ROOT),
        suggested_questions=questions,
    )
    (OUT / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    (OUT / ".graphify_labels.json").write_text(json.dumps({str(k): v for k, v in labels.items()}, indent=2), encoding="utf-8")
    (OUT / ".graphify_analysis.json").write_text(
        json.dumps(
            {
                "communities": {str(k): v for k, v in communities.items()},
                "cohesion": {str(k): v for k, v in cohesion.items()},
                "gods": gods,
                "surprises": surprises,
                "questions": questions,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    wiki_count = to_wiki(G, communities, OUT / "wiki", community_labels=labels, cohesion=cohesion, god_nodes_data=gods)

    save_manifest(detect["files"], root=ROOT)

    cost_path = OUT / "cost.json"
    if cost_path.exists():
        cost = json.loads(cost_path.read_text(encoding="utf-8"))
    else:
        cost = {"runs": [], "total_input_tokens": 0, "total_output_tokens": 0}
    cost["runs"].append(
        {
            "date": datetime.now(timezone.utc).isoformat(),
            "input_tokens": 0,
            "output_tokens": 0,
            "files": detect["total_files"],
            "mode": "rgbds-custom",
        }
    )
    cost_path.write_text(json.dumps(cost, indent=2), encoding="utf-8")

    print(
        f"RGBDS graph: {G.number_of_nodes()} nodes, "
        f"{G.number_of_edges()} edges, {len(communities)} communities"
    )
    print(f"Corpus: {detect['total_files']} files, ~{detect['total_words']} words")
    print(f"Wiki: {wiki_count} articles written to {OUT / 'wiki'}")


if __name__ == "__main__":
    main()
