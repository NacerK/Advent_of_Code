import math


def adjacent_coords(i: int, j: int) -> list[tuple[int, int]]:
    return [
        (i - 1, j),  # top
        (i + 1, j),  # bottom
        (i, j + 1),  # right
        (i, j - 1),  # left
        (i - 1, j - 1),  # top-left
        (i - 1, j + 1),  # top-right
        (i + 1, j - 1),  # bottom-left
        (i + 1, j + 1),  # bottom-right
    ]


def is_symbol(elem: str) -> bool:
    return (elem not in [".", "", "\n"]) and (not elem.isdigit())


def get_elem(input: list[str], i: int, j: int) -> str:
    """Gets an element i,j from a list of strings. Returns an empty string in case of
    an index error"""
    try:
        elem = input[i][j]
    except IndexError:
        elem = ""
    return elem


def get_number(input: list[str], i: int, j: int) -> int:
    """given a position (i,j) corresponding to a digit in the input, return the full
    number by getting the rest of the digits (if they exist) on the left and right
    of (i,j)
    """
    number = get_elem(input, i, j)
    if not number.isdigit():
        raise ValueError(
            f"Expected input[{i}][{j}] to be a number, got {number} " f"instead"
        )
    # get left digits if they exist
    for offset in [-1, 1]:
        k = j
        while True:
            k += offset
            elem = get_elem(input, i, k)
            if elem.isdigit():
                if offset == -1:
                    # add the new digit on the left
                    number = elem + number
                else:
                    # add the new digit on the right
                    number = number + elem
            else:
                break
    return int(number)


def has_adjacent_symbol(input: list[str], i: int, j: int):
    """Check all adjacent elements of the element (i,j). If at least one of them is
    a symbol, returns true, else returns false"""

    for coord in adjacent_coords(i, j):
        adj_elem = get_elem(input, coord[0], coord[1])
        if is_symbol(adj_elem):
            return True
    return False


def get_adjacent_numbers(input: list[str], i: int, j: int):
    """Get all adjacent numbers of the element (i,j)"""
    adjacent_numbers = []
    ajd_coords = adjacent_coords(i, j)

    for coord in ajd_coords:
        adj_elem = get_elem(input, coord[0], coord[1])
        if adj_elem.isdigit():
            adjacent_numbers.append(get_number(input, coord[0], coord[1]))
    # WARNING: we don't handle the case where two or more of the adjacent numbers are
    # equal. We assume all of them are different and transform the list of
    # adjacent_numbers into a set to remove duplicate numbers that are caused by
    # calling get_number() on two different adjacent coordinates belonging to the
    # same number.
    return set(adjacent_numbers)


def main_puzzle1(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()

    # final part numbers list
    part_numbers = []
    # temp stack for digits forming a single number
    digit_stack = ""

    i = 0
    # iterate on all elements
    while i < len(input):
        j = 0
        # -1 subtracts \n from the total number of elements of a line
        while j < len(input[0]) - 1:
            # process only digits
            elem = input[i][j]
            if not elem.isdigit():
                j += 1
                digit_stack = ""
            else:
                digit_stack += elem
                # check if the elem has an adjacent symbol
                if has_adjacent_symbol(input, i, j):
                    # get all the remaining digits of the current number
                    while True:
                        j += 1
                        elem = get_elem(input, i, j)
                        if elem.isdigit():
                            digit_stack += elem
                        else:
                            break
                    # add the current part number and reset the stack
                    part_numbers.append(int(digit_stack))
                    digit_stack = ""

                j += 1
        i += 1

    # print result
    print(f"Puzzle 1: The sum of all part_numbers is {sum(part_numbers)}")


def main_puzzle2(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()
    # will contain the final result
    sum_of_ratios = 0

    for i in range(0, len(input)):
        for j in range(0, len(input[0])):
            elem = get_elem(input, i, j)
            if elem != "*":
                continue
            else:
                adjacent_numbers = get_adjacent_numbers(input, i, j)
                if len(adjacent_numbers) == 2:
                    # if it's a gear (because it has 2 two adjacent numbers)
                    sum_of_ratios += math.prod(adjacent_numbers)

    print(f"Puzzle 2: The sum of gear ratios is {sum_of_ratios}")
    print(
        f"Warning: The puzzle 2 solution does not handle the case where two "
        f"or more adjacent number of a '*' are equal. See the function "
        f"get_adjacent_numbers()"
    )


if __name__ == "__main__":
    main_puzzle1("input.txt")
    main_puzzle2("input.txt")
