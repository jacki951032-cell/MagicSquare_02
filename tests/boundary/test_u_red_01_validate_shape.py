"""U-RED-01 — Boundary rejects non-MATRIX_SIZE×MATRIX_SIZE input."""

import pytest

from magicsquare.boundary import validate
from magicsquare.constants import MATRIX_SIZE


def test_u_red_01_raises_when_not_square_rows() -> None:
    wrong_rows = [[0] * MATRIX_SIZE for _ in range(MATRIX_SIZE - 1)]
    with pytest.raises(ValueError, match=r"must be a 4x4 integer array"):
        validate(wrong_rows)


def test_u_red_01_raises_when_row_width_mismatch() -> None:
    almost = [[0] * (MATRIX_SIZE - 1)] + [[0] * MATRIX_SIZE for _ in range(MATRIX_SIZE - 1)]
    with pytest.raises(ValueError, match=r"must be a 4x4 integer array"):
        validate(almost)
