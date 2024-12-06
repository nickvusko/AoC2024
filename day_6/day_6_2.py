import numpy as np
from typing import Tuple, Set, List


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
        start_dir: str,
        detect_loop: bool = False
) -> Tuple[Set[Tuple[int, int]], bool]:
    """
    Simulates the guard's movement and optionally checks for loops.

    :param lab_map: A numpy array representing the lab map.
    :param start_pos: Starting position of the guard as (row, column).
    :param start_dir: Initial direction of the guard ('^', 'v', '<', '>').
    :param detect_loop: If True, checks for loops and returns whether a loop is detected.
    :returns: A tuple containing:
        - A set of all distinct positions visited by the guard.
        - A boolean indicating whether the guard got stuck in a loop (if detect_loop is True).
    """
    visited_positions = set()
    visited_states = set()  # Tracks (position, direction) for loop detection
    current_pos = start_pos
    current_dir = start_dir
    rows, cols = lab_map.shape

    while True:
        visited_positions.add(current_pos)
        if detect_loop:
            state = (current_pos, current_dir)
            if state in visited_states:
                return visited_positions, True  # Loop detected
            visited_states.add(state)

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

    return visited_positions, False  # No loop detected


def find_loop_obstruction_positions(
        lab_map: np.ndarray,
        guard_pos: Tuple[int, int],
        guard_dir: str
) -> List[Tuple[int, int]]:
    """
    Identifies all possible positions where adding an obstruction would cause the guard to get stuck in a loop.

    :param lab_map: A numpy array representing the lab map.
    :param guard_pos: Starting position of the guard as (row, column).
    :param guard_dir: Initial direction of the guard ('^', 'v', '<', '>').
    :returns: A list of valid positions for placing an obstruction.
    """
    obstruction_positions = []

    # Iterate through all positions in the map
    for i, row in enumerate(lab_map):
        for j, cell in enumerate(row):
            if cell == '.' and (i, j) != guard_pos:  # Open space, not the guard's start
                # Temporarily place an obstruction
                lab_map[i, j] = '#'

                # Simulate guard movement with loop detection
                _, loop_detected = simulate_guard_movement(lab_map, guard_pos, guard_dir, detect_loop=True)

                if loop_detected:
                    obstruction_positions.append((i, j))

                # Remove the obstruction
                lab_map[i, j] = '.'

    return obstruction_positions


# Define directions and movement rules
DIRECTIONS = {
    '^': (-1, 0),  # up
    'v': (1, 0),  # down
    '<': (0, -1),  # left
    '>': (0, 1),  # right
}
DIRECTION_ORDER = ['^', '>', 'v', '<']  # Order to determine right turn

if __name__ == "__main__":
    # Load the lab map from the input file
    lab_map = parse_input("my_input.txt")

    # Locate the guard's starting position and direction
    guard_pos, guard_dir = locate_guard(lab_map)

    # Find valid obstruction positions
    obstruction_positions = find_loop_obstruction_positions(lab_map, guard_pos, guard_dir)

    # Output the result
    print(f"Number of positions that cause a loop: {len(obstruction_positions)}")
    print(f"Obstruction positions: {obstruction_positions}")
