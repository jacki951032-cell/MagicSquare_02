"""Launch the MVP grid window: ``python -m magicsquare.gui``."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from magicsquare.gui.grid_ui import GridUI


def main() -> None:
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Magic Square 4×4 — Grid (MVP)")
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    layout.addWidget(GridUI())
    window.resize(320, 280)
    window.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
