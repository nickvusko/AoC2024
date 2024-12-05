import numpy as np
import re


def parse_input() -> np.array:
    """
    Loads the content of a .txt file.

    :returns: numpy array, each cell contains one letter.
    """
    with open("test_input.txt", "r") as file:
        return np.array([list(line.strip()) for line in file])



# Example word search input
def count_xmas_occurrences(grid: np.array) -> int:
    """Count xmas occurence.
    Use regex to match the sequence.
    Treat the matrix as lines of strings.

    :param grid: np.array input.
    :return: occurrence count.
    """
    def extract_diagonals(grid: np.array) -> list[str]:
        """Transfer diagonals to strings.

        :param grid: input matrix.
        :return: diagonals as list of strings.
        """
        diagonals = []
        nrows, ncols = grid.shape
        # Top-left to bottom-right diagonals
        for d in range(-nrows + 1, ncols):
            diagonals.append("".join(grid[i, i - d] for i in range(max(0, d), min(nrows, ncols + d))))
        # Top-right to bottom-left diagonals
        for d in range(ncols + nrows - 1):
            diagonals.append("".join(grid[i, d - i] for i in range(max(0, d - ncols + 1), min(nrows, d + 1))))
        return diagonals

    # Extract rows and columns
    rows = ["".join(row) for row in grid]
    columns = ["".join(grid[:, col]) for col in range(grid.shape[1])]

    # Extract diagonals
    diagonals = extract_diagonals(grid)

    # Combine all lines to search
    all_lines = rows + columns + diagonals

    # Count occurrences of "XMAS" and "SAMX"
    word = "XMAS"
    reverse_word = word[::-1]
    def count_word_occurrences(line, word, reverse_word):
        return len(re.findall(f"(?={word})", line)) + len(re.findall(f"(?={reverse_word})", line))

    return sum(count_word_occurrences(line, word, reverse_word) for line in all_lines)


print(count_xmas_occurrences(parse_input()))


def find_x_mas_patterns_part_two(grid) -> int:
    nrows, ncols = grid.shape

    def is_valid_x_mas(grid, row, col) -> bool:
        try:
            # Check diagonals from the center point (row, col)
            diag1 = [grid[row - 1, col - 1], grid[row, col], grid[row + 1, col + 1]]
            diag2 = [grid[row - 1, col + 1], grid[row, col], grid[row + 1, col - 1]]
            # Validate both diagonals form "MAS" or "SAM"
            return (
                (diag1 == list("MAS") or diag1 == list("SAM")) and
                (diag2 == list("MAS") or diag2 == list("SAM"))
            )
        except IndexError:
            # Out of bounds
            return False

    # Iterate through the grid and find all "A" positions
    x_mas_count = 0
    for row in range(1, nrows - 1):  # Avoid edges
        for col in range(1, ncols - 1):  # Avoid edges
            if grid[row, col] == "A" and is_valid_x_mas(grid, row, col):
                x_mas_count += 1

    return x_mas_count


# Find X-MAS patterns in the example grid
print(find_x_mas_patterns_part_two(parse_input()))
