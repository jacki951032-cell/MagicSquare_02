"""L-RED-01 — Domain blank discovery in row-major order."""

from magicsquare.constants import MATRIX_SIZE
from magicsquare.domain import find_blank_coords


def test_l_red_01_find_blank_coords_row_major_two_cells() -> None:
    """Two zeros in row-major order: first row left two columns (1-index)."""
    m = [
        [0, 0, 1, 2],
        [3, 4, 5, 6],
        [7, 8, 9, 10],
        [11, 12, 13, 14],
    ]
    assert len(m) == MATRIX_SIZE and all(len(row) == MATRIX_SIZE for row in m)
    assert find_blank_coords(m) == [(1, 1), (1, 2)]
