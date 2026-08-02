from __future__ import annotations

from battle_characterization.paths import REPO_ROOT


def test_no_c_implementation_exists_before_contract_review() -> None:
    rewrite_root = REPO_ROOT / "rewrite"
    implementation_files = sorted(
        path.relative_to(REPO_ROOT)
        for suffix in ("*.c", "*.h")
        for path in rewrite_root.rglob(suffix)
        if ".venv" not in path.parts
    )
    assert implementation_files == [], (
        "C implementation is blocked until the ASM characterization contract is reviewed: "
        f"{implementation_files}"
    )
