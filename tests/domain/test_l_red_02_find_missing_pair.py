"""L-RED-02 — missing two numbers (a, b), a < b from 1..VALUE_MAX (FR-03)."""

from magicsquare.constants import MATRIX_SIZE, VALUE_MAX
from magicsquare.domain import find_missing_pair


def test_l_red_02_find_missing_pair_sorted() -> None:
    """Zeros at (1,1),(1,2); values 1..14 elsewhere → missing (15, 16)."""
    m = [
        [0, 0, 1, 2],
        [3, 4, 5, 6],
        [7, 8, 9, 10],
        [11, 12, 13, 14],
    ]
    assert len(m) == MATRIX_SIZE and all(len(row) == MATRIX_SIZE for row in m)
    assert find_missing_pair(m) == (VALUE_MAX - 1, VALUE_MAX)
