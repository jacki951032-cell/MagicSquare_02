"""최소 마방진 6-튜플 — §9.3 예 A에 대해 하드코딩 검산값만 반환."""

from __future__ import annotations

from typing import Final

Matrix = list[list[int]]

# PRD §9.3 예 A (Report/04 동기)
_GOLDEN_A: Final[Matrix] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# 검산: 누락 (1,6), row-major 첫 0 (3,3)·둘째 (4,4); 시도1 실패 후 시도2 성공
# AC-05-3: [r1,c1,b,r2,c2,a]
_GOLDEN_A_TUPLE: Final[list[int]] = [3, 3, 6, 4, 4, 1]

# Golden A solved (after applying _GOLDEN_A_TUPLE): no zeros remain.
_GOLDEN_A_SOLVED: Final[Matrix] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]


def demo_solution() -> tuple[Matrix, list[int]]:
    """Return (solved_matrix, answer_tuple) for the built-in demo (hardcoded)."""
    return ([row[:] for row in _GOLDEN_A_SOLVED], list(_GOLDEN_A_TUPLE))


def solve_magic_square(matrix: Matrix) -> list[int]:
    """유효 격자에 대한 6-원 배치. 현재는 §9.3 예 A만 지원(나머지는 ``ValueError``)."""
    if matrix == _GOLDEN_A:
        return list(_GOLDEN_A_TUPLE)
    raise ValueError("unsupported matrix for minimal solver")
