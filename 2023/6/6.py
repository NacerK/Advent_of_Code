import math
import numpy as np


def get_hold_times(distance: int, full_time: int) -> tuple[int, int]:
    """get hold times that correspond to a give distance
    by solving x*(full_time - x) - distance = 0"""
    a = -1
    b = full_time
    c = -distance

    return np.roots([a, b, c])


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()
    # load input to a np array
    input_np = np.array([line.split(":")[1].split() for line in input], dtype=int)

    # get number of ways to win of each race
    n_races = len(input_np[0])
    win_numbers = np.ndarray(n_races, dtype=np.int64)
    for i in range(n_races):
        x1, x2 = get_hold_times(input_np[1, i], input_np[0, i])
        win_numbers[i] = np.ceil(x1) - np.floor(x2) - 1

    print(
        f"Puzzle 1: the product of the number of ways to win each race is "
        f"{win_numbers.prod()}"
    )

    # Puzzle 2:
    time, distance = [
        int(line.split(":")[1].strip().replace(" ", "")) for line in input
    ]
    x1, x2 = get_hold_times(distance, time)
    win_number_p2 = int(np.ceil(x1) - np.floor(x2) - 1)

    print(
        f"Puzzle 1: the product of the number of ways to win each race is "
        f"{win_number_p2}"
    )


if __name__ == "__main__":
    main("input.txt")
