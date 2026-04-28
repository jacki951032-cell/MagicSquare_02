"""U-RED-02 — zero count must be exactly two (FR-01, E_ZERO_COUNT)."""

import pytest

from magicsquare.boundary import validate
from magicsquare.constants import EXPECTED_ZERO_COUNT, MATRIX_SIZE


def _full_1_to_16_rows() -> list[list[int]]:
    # 1..16 in row-major 4x4, no zeros (zero count 0)
    return [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]


def test_u_red_02_raises_when_not_exactly_two_zeros() -> None:
    m = _full_1_to_16_rows()
    assert sum(1 for r in m for c in r if c == 0) != EXPECTED_ZERO_COUNT
    with pytest.raises(
        ValueError, match="^matrix must contain exactly two zeros\\.$"
    ):
        validate(m)


def test_u_red_02_raises_when_three_zeros() -> None:
    m = [
        [0, 0, 0, 1],
        [2, 3, 4, 5],
        [6, 7, 8, 9],
        [10, 11, 12, 13],
    ]
    assert len(m) == MATRIX_SIZE
    assert sum(1 for r in m for c in r if c == 0) == 3
    with pytest.raises(
        ValueError, match="^matrix must contain exactly two zeros\\.$"
    ):
        validate(m)
