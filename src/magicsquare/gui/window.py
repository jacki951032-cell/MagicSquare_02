"""PyQt Screen window wiring GridUI -> Boundary -> Logic.

Screen layer only: handles UX events and error display.
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary import validate
from magicsquare.gui.grid_ui import GridUI
from magicsquare.magic_square import demo_solution, solve_magic_square


class MagicSquareWindow(QWidget):
    """MVP window: grid input + Solve button + result display."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._grid = GridUI()
        self._solve_btn = QPushButton("풀기")
        self._result = QLabel("결과: (아직 없음)")
        self._result.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self._grid)
        layout.addWidget(self._solve_btn)
        layout.addWidget(self._result)

        self._solve_btn.clicked.connect(self._on_solve_clicked)  # type: ignore[attr-defined]

    def grid(self) -> GridUI:
        """Expose the grid widget (for prefill / manual inspection)."""

        return self._grid

    def _on_solve_clicked(self) -> None:
        matrix = self._grid.matrix()

        try:
            validate(matrix)
            answer = solve_magic_square(matrix)
            solved_matrix = None
        except ValueError as e:
            # UX: even on failure, present the demo correct answer and fill the grid.
            solved_matrix, answer = demo_solution()
            QMessageBox.information(
                self,
                "정답 표시",
                f"{e}\n\n입력과 무관하게 데모 정답을 표시합니다.",
            )

        if solved_matrix is not None:
            self._grid.set_matrix(solved_matrix)
        else:
            # Apply the 6-tuple to the current grid so blanks disappear.
            r1, c1, n1, r2, c2, n2 = answer
            self._grid.set_cell_1idx(r1, c1, n1)
            self._grid.set_cell_1idx(r2, c2, n2)
        self._result.setText(f"결과: {answer}")

