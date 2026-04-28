"""Launch the MVP grid window: ``python -m magicsquare.gui``."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from magicsquare.gui.grid_ui import GridUI

# UX-only: two 0-cells + 1..14 each once, spread non-sequentially (not row-major 1,2,3,…).
_DEMO_MATRIX: list[list[int]] = [
    [11, 3, 0, 7],
    [2, 14, 9, 0],
    [13, 5, 6, 12],
    [8, 1, 4, 10],
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
