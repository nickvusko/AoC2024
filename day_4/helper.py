import numpy as np


xmas = "XMAS"

def go_next(expected_letter: str, real_letter: str) -> bool:
    """Check if next letter matches expectation.

    :param expected_letter: expected letter
    :param real_letter: real letter
    :return: True if match, otherwise False
    """
    return expected_letter == real_letter


def check_row(matrix: np.array, forward: bool = True) -> int:
    """
    Check row.

    :param matrix: input matrix.
    :param forward: True if look right, otherwise look left.
    :return: number of hits.
    """
    match = 0
    for row in range(matrix.shape[0]):
        position = 0
        for column in range(matrix.shape[1]) if forward else range(matrix.shape[1] -1, -1, -1):
            if go_next(xmas[position], matrix[row][column]):
                position += 1
            elif matrix[row][column] == "X":
                position = 1
            else:
                position = 0
            if position == len(xmas):
                match += 1
                position = 0
    return match


def check_column(matrix: np.array, up: bool = True) -> int:
    """
    Check column.

    :param matrix: input matrix.
    :param up: True if look down, otherwise look up.
    :return: number of hits.
    """
    match = 0
    for column in range(matrix.shape[1]):
        position = 0
        for row in range(matrix.shape[0]) if up else range(matrix.shape[0] -1, -1, -1):
            if go_next(xmas[position], matrix[row][column]):
                position += 1
            elif matrix[row][column] == "X":
                position = 1
            else:
                position = 0
            if position == len(xmas):
                match += 1
                position = 0
    return match
