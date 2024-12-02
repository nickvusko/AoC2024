

def parse_input() -> tuple[tuple[int, ...], ...]:
    """
    Loads the content of a .txt file.

    :returns: tuple of tuples, each tuple represents single line.
    """
    with open("test_input.txt", "r") as file:
        return tuple(tuple(map(int, line.split())) for line in file if line.strip())


def find_safe_records() -> int:
    """
    Find safe records.

    :returns: number of safe lines.
    """

    return sum(1 for line in parse_input() if check_trend(line))


def check_trend(record: tuple[int, ...]) -> bool:
    """
    Check line trend.

    :param record: record to check
    :return: True if line is safe, otherwise False.
    """
    differences = [record[i + 1] - record[i] for i in range(len(record) - 1)]
    if not all(1 <= abs(diff) <= 3 for diff in differences):
        return False
    return all(diff > 0 for diff in differences) or all(diff < 0 for diff in differences)


print(find_safe_records())


def find_safe_records_with_dampener() -> int:
    """
    Find safe records.

    :returns: number of safe lines.
    """
    def check_trend_with_dampener(record: tuple[int, ...]) -> bool:
        """
        Check line trend.

        :param record: record to check
        :return: True if line is safe, otherwise False.
        """
        if check_trend(record):
            return True
        for i in range(len(record)):
            modified_record = record[:i] + record[i + 1:]
            if check_trend(modified_record):
                return True
        return False

    return sum(1 for line in parse_input() if check_trend_with_dampener(line))


print(find_safe_records_with_dampener())
