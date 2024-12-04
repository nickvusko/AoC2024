import re


def day3_1() -> int:
    """
    Loads the content of a .txt file and matches it with regex.

    :returns: result as a number.
    """
    with open("my_input.txt", "r") as file:
        content = file.read()
    matches = re.findall(r"mul\((\d+),(\d+)\)", content)
    return sum(int(x) * int(y) for x, y in matches)


print(day3_1())


def day3_2() -> int:
    """
    Loads the content of a .txt file and matches it with regex.

    :returns: result as a number.
    """
    with open("my_input.txt", "r") as file:
        content = file.read()
    mul_pattern = r"mul\((\d+),(\d+)\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"
    do_matches = [(1, match.start(), match.end()) for match in re.finditer(do_pattern, content)]
    dont_matches = [(0, match.start(), match.end()) for match in re.finditer(dont_pattern, content)]

    enabled_ranges = []
    mul_enabled = True
    last_end = 0

    for state, start, end in sorted((do_matches + dont_matches), key=lambda x: x[1]):
        if mul_enabled:
            enabled_ranges.append((last_end, start))
        last_end = end
        mul_enabled = (state == 1)

    if mul_enabled:
        enabled_ranges.append((last_end, len(content)))

    matches = []
    for start, end in enabled_ranges:
        substring = content[start:end]
        matches += re.findall(mul_pattern, substring)
    return sum(int(x) * int(y) for x, y in matches)


print(day3_2())
