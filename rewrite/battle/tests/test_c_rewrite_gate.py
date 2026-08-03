from __future__ import annotations

from battle_characterization.paths import REPO_ROOT


def test_reviewed_c_milestone_has_public_api_and_native_tests() -> None:
    battle_root = REPO_ROOT / "rewrite" / "battle"
    public_headers = sorted((battle_root / "include" / "pokered" / "battle").glob("*.h"))
    implementation_files = sorted((battle_root / "src").glob("*.c"))

    assert public_headers
    assert implementation_files
    assert (battle_root / "tests" / "c" / "test_main.c").is_file()
    assert (battle_root / "Makefile").is_file()


def test_c_domain_does_not_depend_on_emulator_or_rgbds_sources() -> None:
    battle_root = REPO_ROOT / "rewrite" / "battle"
    source_text = "\n".join(
        path.read_text(encoding="utf-8")
        for directory in (battle_root / "include", battle_root / "src")
        for path in directory.rglob("*.[ch]")
    )

    forbidden = ("pyboy", "engine/battle", "wEnemyMon", "wBattleMon", "hWhoseTurn")
    assert all(token not in source_text for token in forbidden)
