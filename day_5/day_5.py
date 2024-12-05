from collections import defaultdict, deque
from typing import List, Tuple


def parse_input() -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    """
    Parses the input data into rules and updates.

    Returns:
        Tuple[List[Tuple[int, int]], List[List[int]]]:
            A tuple where the first element is a list of rules as (X, Y) pairs and
            the second element is a list of updates (lists of page numbers).
    """
    with open("test_input.txt", "r") as file:
        content = file.read()
    sections = content.strip().split("\n\n")
    rules = [tuple(map(int, line.split('|'))) for line in sections[0].splitlines()]
    updates = [list(map(int, line.split(','))) for line in sections[1].splitlines()]
    return rules, updates


def is_update_valid(rules: List[Tuple[int, int]], update: List[int]) -> bool:
    """
    Checks if an update follows the specified rules.

    Args:
        rules (List[Tuple[int, int]]): List of (X, Y) rules.
        update (List[int]): Update to be validated.

    Returns:
        bool: True if the update is valid, False otherwise.
    """
    # Create a map of indices for the update
    page_positions = {page: idx for idx, page in enumerate(update)}
    for x, y in rules:
        if x in page_positions and y in page_positions:
            if page_positions[x] >= page_positions[y]:
                return False
    return True


def find_middle_pages(rules: List[Tuple[int, int]], updates: List[List[int]]) -> int:
    """
    Finds the middle pages of all valid updates and sums them.

    Args:
        rules (List[Tuple[int, int]]): List of (X, Y) rules.
        updates (List[List[int]]): List of updates to validate.

    Returns:
        int: Sum of middle pages for all valid updates.
    """
    valid_middle_pages = []
    for update in updates:
        if is_update_valid(rules, update):
            valid_middle_pages.append(update[len(update) // 2])
    return sum(valid_middle_pages)


# Parse input and calculate result
rules, updates = parse_input()
print(find_middle_pages(rules, updates))


def print_sort(pages: List[int], rules: List[Tuple[int, int]]) -> List[int]:
    """
    Performs topological sorting on the given pages using the rules.

    Args:
        pages (List[int]): Pages in the current update.
        rules (List[Tuple[int, int]]): Rules as (X, Y) pairs where X must precede Y.

    Returns:
        List[int]: Pages sorted in the correct order.
    """
    # Create graph and in-degree count for pages in the update
    graph = defaultdict(list)
    in_degree = {page: 0 for page in pages}

    for x, y in rules:
        if x in in_degree and y in in_degree:
            graph[x].append(y)
            in_degree[y] += 1

    # Perform topological sort using Kahn's algorithm
    queue = deque([page for page in pages if in_degree[page] == 0])
    sorted_pages = []

    while queue:
        current = queue.popleft()
        sorted_pages.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_pages


def reorder_and_find_middle_sum(rules: List[Tuple[int, int]], updates: List[List[int]]) -> int:
    """
    Reorders incorrectly-ordered updates and calculates the sum of their middle pages.

    Args:
        rules (List[Tuple[int, int]]): List of (X, Y) rules.
        updates (List[List[int]]): List of updates to process.

    Returns:
        int: Sum of the middle pages of reordered updates.
    """
    middle_sum = 0
    for update in updates:
        if not is_update_valid(rules, update):
            # Fix the order of the update
            sorted_update = print_sort(update, rules)
            # Add the middle page of the sorted update
            middle_sum += sorted_update[len(sorted_update) // 2]
    return middle_sum


# Example Input
rules, updates = parse_input()
print(reorder_and_find_middle_sum(rules, updates))
