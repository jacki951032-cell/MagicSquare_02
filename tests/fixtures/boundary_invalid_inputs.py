"""Minimal literals for FR-01 boundary tests (UI-T-01~04)."""

# UI-T-01: not 4×4
M_INPUT_SHAPE_NOT_4X4 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

# UI-T-02: 4×4 but zero count ≠ 2 (exactly one zero)
M_ZERO_COUNT_ONE = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0],
]

# UI-T-03: value outside {0} ∪ [1, 16]
M_INVALID_RANGE = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 17],
]

# UI-T-04: duplicate non-zero (two blanks + repeated 5)
M_DUPLICATE_NONZERO = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 5, 12],
    [0, 14, 15, 0],
]
