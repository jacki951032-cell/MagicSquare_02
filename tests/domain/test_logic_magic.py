"""Logic — minimal ``magic_square`` hardcoded golden (§9.3 예 A)."""

from __future__ import annotations

import pytest

from magicsquare.magic_square import solve_magic_square

# PRD §9.3 예 A
GOLDEN_A: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# AC-05-3: 시도2 성공 시 [r1,c1,b,r2,c2,a] (검산)
EXPECTED_TUPLE: list[int] = [3, 3, 6, 4, 4, 1]


def test_logic_magic_golden_a_six_tuple() -> None:
    assert solve_magic_square(GOLDEN_A) == EXPECTED_TUPLE


def test_logic_magic_other_matrix_rejected() -> None:
    with pytest.raises(ValueError, match="unsupported"):
        solve_magic_square([[0] * 4 for _ in range(4)])
