"""Subset comparison for reviewed characterization expectations."""

from __future__ import annotations

from typing import Any

from .case import BattleCase, BattleResult


def assert_expected(case: BattleCase, result: BattleResult) -> None:
    if case.expected is None:
        raise AssertionError(f"{case.id} has no reviewed expectation")
    expected = case.expected.get(result.variant)
    if expected is None:
        raise AssertionError(f"{case.id} has no expectation for {result.variant}")
    _assert_subset(expected, result.to_dict(), case.id)


def _assert_subset(expected: Any, actual: Any, path: str) -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise AssertionError(f"{path}: expected mapping, got {type(actual).__name__}")
        for key, value in expected.items():
            if key not in actual:
                raise AssertionError(f"{path}: missing key {key!r}")
            _assert_subset(value, actual[key], f"{path}.{key}")
        return
    if expected != actual:
        raise AssertionError(f"{path}: expected {expected!r}, got {actual!r}")
