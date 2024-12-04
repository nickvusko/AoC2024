import numpy as np

import helper


def parse_input() -> np.array:
    """
    Loads the content of a .txt file.

    :returns: numpy array, each cell contains one letter.
    """
    with open("test_input.txt", "r") as file:
        return np.array([list(line.strip()) for line in file])


def search_for_xmas() -> int:
    """
    Search for XMAS string.

    :return: number of hits.
    """
    xmas = "XMAS"
    matrix = parse_input()
    return sum((helper.check_row(matrix), helper.check_row(matrix, forward=False), helper.check_column(matrix),
                helper.check_column(matrix, up=False)))



print(search_for_xmas())