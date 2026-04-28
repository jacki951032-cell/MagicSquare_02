"""Input validation and boundary contracts — no business rules beyond FR-01 shape check here."""

from magicsquare.constants import MATRIX_SIZE


def validate(matrix: list[list[int]]) -> None:
    """Raise ValueError when the matrix is not a MATRIX_SIZE×MATRIX_SIZE integer grid (U-RED-01)."""
    if len(matrix) != MATRIX_SIZE:
        raise ValueError(
            f"matrix must be a {MATRIX_SIZE}x{MATRIX_SIZE} integer array."
        )
    for row in matrix:
        if len(row) != MATRIX_SIZE:
            raise ValueError(
                f"matrix must be a {MATRIX_SIZE}x{MATRIX_SIZE} integer array."
            )
