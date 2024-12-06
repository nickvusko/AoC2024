import numpy as np
from typing import Tuple, Set

def parse_input(filename: str) -> np.ndarray:
    """
    Parses the content of a .txt file into a numpy array.

    :param filename: Path to the input file.
    :returns: A numpy array representing the lab map, where each cell contains one character.
    """
    with open(filename, "r") as file:
        return np.array([list(line.strip()) for line in file])


def locate_guard(lab_map: np.ndarray) -> Tuple[Tuple[int, int], str]:
    """
    Finds the starting position and initial direction of the guard using NumPy.

    :param lab_map: A numpy array representing the lab map.
    :returns: A tuple containing the guard's starting position as (row, column) and its direction.
    """
    guard_mask = (lab_map != '#') & (lab_map != '.')
    guard_positions = np.argwhere(guard_mask)

    if len(guard_positions) == 0:
        raise ValueError("Guard not found in the map")

    guard_pos = tuple(guard_positions[0])  # First match, assuming one guard
    guard_dir = lab_map[guard_pos]
    return guard_pos, guard_dir

def simulate_guard_movement(
    lab_map: np.ndarray,
    start_pos: Tuple[int, int],
    start_dir: str
) -> Set[Tuple[int, int]]:
    """
    Simulates the guard's movement based on the patrol rules and tracks visited positions.

    :param lab_map: A numpy array representing the lab map.
    :param start_pos: Starting position of the guard as (row, column).
    :param start_dir: Initial direction of the guard ('^', 'v', '<', '>').
    :returns: A set of tuples representing all distinct positions visited by the guard.
    """
    visited = set()
    current_pos = start_pos
    current_dir = start_dir
    rows, cols = lab_map.shape

    while True:
        visited.add(current_pos)
        next_pos = (current_pos[0] + DIRECTIONS[current_dir][0],
                    current_pos[1] + DIRECTIONS[current_dir][1])

        # Check if next position is out of bounds
        if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
            break

        # Check if there's an obstacle
        if lab_map[next_pos] == '#':
            # Turn right
            current_dir = DIRECTION_ORDER[(DIRECTION_ORDER.index(current_dir) + 1) % 4]
        else:
            # Move forward
            current_pos = next_pos

    return visited

# Define directions and movement rules
DIRECTIONS = {
    '^': (-1, 0),  # up
    'v': (1, 0),   # down
    '<': (0, -1),  # left
    '>': (0, 1),   # right
}
DIRECTION_ORDER = ['^', '>', 'v', '<']  # Order to determine right turn

if __name__ == "__main__":
    # Load the lab map from the input file
    lab_map = parse_input("my_input.txt")

    # Locate the guard's starting position and direction
    guard_pos, guard_dir = locate_guard(lab_map)

    # Simulate the guard's movement and calculate distinct positions visited
    visited_positions = simulate_guard_movement(lab_map, guard_pos, guard_dir)

    # Output the result
    print(f"Distinct positions visited: {len(visited_positions)}")
