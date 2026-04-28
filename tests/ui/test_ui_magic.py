"""Track A — UI / Screen-facing tests (Dual-Track).

Uses :class:`magicsquare.gui.GridUI` for UX-only assembly; Boundary ``validate`` remains the gate.
"""

import sys

import pytest

from magicsquare.boundary import validate
from magicsquare.constants import MATRIX_SIZE


def test_ui_magic_validate_accepts_assembled_4x4_before_solve() -> None:
    """Form-assembled 4×4 int[][] must pass Boundary validate (FR-01 shape) before any solve call."""
    pytest.importorskip("PyQt6.QtWidgets")

    from PyQt6.QtWidgets import QApplication

    from magicsquare.gui import GridUI

    _app = QApplication.instance() or QApplication(sys.argv)

    grid = GridUI()
    m = [
        [0, 0, 1, 2],
        [3, 4, 5, 6],
        [7, 8, 9, 10],
        [11, 12, 13, 14],
    ]
    grid.set_matrix(m)

    assembled = grid.matrix()
    assert len(assembled) == MATRIX_SIZE and all(
        len(row) == MATRIX_SIZE for row in assembled
    )
    validate(assembled)
