"""Input validation and boundary contracts — FR-01 checks only at boundary."""

from magicsquare.constants import EXPECTED_ZERO_COUNT, MATRIX_SIZE


_ERR_SHAPE = f"matrix must be a {MATRIX_SIZE}x{MATRIX_SIZE} integer array."
_ERR_ZERO_COUNT = "matrix must contain exactly two zeros."


def _validate_shape(matrix: list[list[int]]) -> None:
    if len(matrix) != MATRIX_SIZE:
        raise ValueError(_ERR_SHAPE)
    for row in matrix:
        if len(row) != MATRIX_SIZE:
            raise ValueError(_ERR_SHAPE)


def _validate_zero_count(matrix: list[list[int]]) -> None:
    zeros = sum(1 for row in matrix for cell in row if cell == 0)
    if zeros != EXPECTED_ZERO_COUNT:
        raise ValueError(_ERR_ZERO_COUNT)


def validate(matrix: list[list[int]]) -> None:
    """Raise ValueError when FR-01 fails (shape U-RED-01, zero count U-RED-02)."""
    _validate_shape(matrix)
    _validate_zero_count(matrix)
