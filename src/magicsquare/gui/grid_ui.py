"""4×4 numeric grid — presentation and value read/write only (no validation or domain)."""

from __future__ import annotations

from PyQt6.QtWidgets import QGridLayout, QSpinBox, QWidget

from magicsquare.constants import MATRIX_SIZE, VALUE_MAX


class GridUI(QWidget):
    """MVP 4×4 cell editor: `0`..`VALUE_MAX` per cell; use :meth:`matrix` / :meth:`set_matrix` for data exchange."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._cells: list[list[QSpinBox]] = []
        layout = QGridLayout(self)
        for r in range(MATRIX_SIZE):
            row: list[QSpinBox] = []
            for c in range(MATRIX_SIZE):
                cell = QSpinBox()
                cell.setRange(0, VALUE_MAX)
                cell.setValue(0)
                layout.addWidget(cell, r, c)
                row.append(cell)
            self._cells.append(row)

    def set_matrix(self, values: list[list[int]]) -> None:
        """Fill spinboxes from a ``MATRIX_SIZE``×``MATRIX_SIZE`` table (caller owns correctness)."""
        for r in range(MATRIX_SIZE):
            for c in range(MATRIX_SIZE):
                self._cells[r][c].setValue(values[r][c])

    def matrix(self) -> list[list[int]]:
        """Snapshot current grid as ``list[list[int]]`` (same shape as :meth:`set_matrix`)."""
        return [
            [self._cells[r][c].value() for c in range(MATRIX_SIZE)]
            for r in range(MATRIX_SIZE)
        ]
