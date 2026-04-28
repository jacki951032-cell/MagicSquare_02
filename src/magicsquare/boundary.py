"""Input validation and boundary contracts — FR-01 checks only at boundary."""

from magicsquare.constants import EXPECTED_ZERO_COUNT, MATRIX_SIZE


def validate(matrix: list[list[int]]) -> None:
    """Raise ValueError when FR-01 fails (shape U-RED-01, zero count U-RED-02)."""
    if len(matrix) != MATRIX_SIZE:
        raise ValueError(
            f"matrix must be a {MATRIX_SIZE}x{MATRIX_SIZE} integer array."
        )
    for row in matrix:
        if len(row) != MATRIX_SIZE:
            raise ValueError(
                f"matrix must be a {MATRIX_SIZE}x{MATRIX_SIZE} integer array."
            )

    zeros = sum(1 for row in matrix for cell in row if cell == 0)
    if zeros != EXPECTED_ZERO_COUNT:
        raise ValueError("matrix must contain exactly two zeros.")
