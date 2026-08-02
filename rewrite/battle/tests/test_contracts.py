from __future__ import annotations

from pathlib import Path
import json

from battle_characterization.contracts import load_case_document
from battle_characterization.inventory import controlled_ids
from battle_characterization.paths import CONTRACT_ROOT, REPO_ROOT
from battle_characterization.traceability import ALLOWED_METHODS, evidence_paths, load_traceability


def case_files() -> list[Path]:
    return sorted((CONTRACT_ROOT / "cases").glob("*.json"))


def test_every_case_document_matches_the_public_schema() -> None:
    files = case_files()
    assert files, "no battle contracts found"
    case_ids: list[str] = []
    for path in files:
        document = load_case_document(path)
        case_ids.extend(case["id"] for case in document["cases"])
    assert len(case_ids) == len(set(case_ids)), "case IDs must be globally unique"


def test_baseline_is_pinned_to_the_worktree_origin() -> None:
    baseline = json.loads((CONTRACT_ROOT / "baseline.json").read_text(encoding="utf-8"))
    assert baseline == {
        "baseline_commit": "2b9f524537649e22d11bedaaee6eb81832fbbcb0",
        "rgbds_version": "v1.0.2+hotfix",
        "pyboy_version": "2.7.0",
        "rom_hash_source": "roms.sha1",
        "behavior_mode": "GEN1_FIDELITY",
        "golden_update_policy": "explicit-review-only",
    }


def test_traceability_covers_every_controlled_requirement() -> None:
    matrix = load_traceability()
    entries = [entry for group in matrix["groups"] for entry in group["ids"]]
    assert set(entries) == controlled_ids()
    assert len(entries) == len(set(entries)), "each controlled ID must have one owner"
    assert all(group["method"] in ALLOWED_METHODS for group in matrix["groups"])
    assert all(group["status"] == "covered" for group in matrix["groups"])


def test_traceability_evidence_exists() -> None:
    missing = [path.relative_to(REPO_ROOT) for path in evidence_paths(load_traceability()) if not path.exists()]
    assert not missing, f"missing traceability evidence: {missing}"
