"""Pure domain logic — no UI / DB / Web / PyQt."""

from magicsquare.constants import MATRIX_SIZE


def find_blank_coords(matrix: list[list[int]]) -> list[tuple[int, int]]:
    """Return the two blank (0) cell coordinates in row-major order; coordinates are 1-indexed."""
    found: list[tuple[int, int]] = []
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            if matrix[r][c] == 0:
                found.append((r + 1, c + 1))
                if len(found) == 2:
                    return found
    return found
