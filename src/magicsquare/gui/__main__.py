"""Launch the MVP grid window: ``python -m magicsquare.gui``."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from magicsquare.gui.grid_ui import GridUI

# UX-only starter puzzle: two blanks (0) + distinct 1..14 elsewhere — same shape as UI smoke test.
_DEMO_MATRIX: list[list[int]] = [
    [0, 0, 1, 2],
    [3, 4, 5, 6],
    [7, 8, 9, 10],
    [11, 12, 13, 14],
]


def main() -> None:
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Magic Square 4×4 — Grid (MVP)")
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    grid = GridUI()
    grid.set_matrix(_DEMO_MATRIX)
    layout.addWidget(grid)
    window.resize(320, 280)
    window.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
