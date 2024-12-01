

def parse_input() -> tuple[list, list]:
    """
    Loads the content of a .txt file.

    :returns: list of lists containing the numbers from the file.
    """
    try:
        with open("test_input.txt", "r") as file:
            result = list(zip(*[map(int, line.split()) for line in file if line.strip()]))
            return list(result[0]), list(result[1])
    except Exception as e:
        print(f"Error: {e}")
        return [], []


def find_ids() -> int:
    """
    Search for lowest numbers and add the diff.

    :returns: sum as int.
    """
    result = 0
    left, right = parse_input()
    while left:
        result += abs(left.pop(left.index(min(left))) - right.pop(right.index(min(right))))
    return result


print(find_ids())


def find_similarities() -> int:
    """
    Search for similarities in the lists.

    :returns: sum as int.
    """
    result = 0
    left, right = parse_input()
    while left:
        number = left.pop()
        result += number * right.count(number)
    return result


print(find_similarities())
