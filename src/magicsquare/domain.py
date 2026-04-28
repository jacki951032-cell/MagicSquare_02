"""Pure domain logic — no UI / DB / Web / PyQt."""

from magicsquare.constants import MATRIX_SIZE, VALUE_MAX


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


def find_missing_pair(matrix: list[list[int]]) -> tuple[int, int]:
    """Return (a, b) with a < b — the two values in 1..VALUE_MAX absent from non-zero cells (FR-03)."""
    present: set[int] = set()
    for r in range(MATRIX_SIZE):
        for c in range(MATRIX_SIZE):
            v = matrix[r][c]
            if v != 0:
                present.add(v)
    universe = frozenset(range(1, VALUE_MAX + 1))
    missing = tuple(sorted(universe - present))
    return (missing[0], missing[1])
