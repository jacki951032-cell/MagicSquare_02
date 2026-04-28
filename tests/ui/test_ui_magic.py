"""Track A — UI / Screen-facing tests (Dual-Track).

PyQt widget tests can live here once ``magicsquare.gui`` exists; domain rules stay in ``tests/domain``.
"""

from magicsquare.boundary import validate
from magicsquare.constants import MATRIX_SIZE


def test_ui_magic_validate_accepts_assembled_4x4_before_solve() -> None:
    """Form-assembled 4×4 int[][] must pass Boundary validate (FR-01 shape) before any solve call."""
    m = [
        [0, 0, 1, 2],
        [3, 4, 5, 6],
        [7, 8, 9, 10],
        [11, 12, 13, 14],
    ]
    assert len(m) == MATRIX_SIZE and all(len(row) == MATRIX_SIZE for row in m)
    validate(m)
