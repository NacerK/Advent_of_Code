import numpy as np


def get_steps(
    go_left: dict, go_right: dict, instructions: list[str], start: str, end: str
) -> int:
    location = start
    steps = 0

    while True:
        for direction in instructions:
            steps += 1
            if direction == "L":
                location = go_left[location]
            else:
                location = go_right[location]
            if location.endswith(end):
                break
        if location.endswith(end):
            break
    return steps


def input_to_dicts(input: list[str]) -> tuple[dict[str], dict[str]]:
    char_to_remove = [" ", "(", ")", "\n"]
    left_dict = {}
    right_dict = {}
    for line in input:
        clean_line = "".join([c for c in line if c not in char_to_remove])
        node, neighbors = clean_line.split("=")
        left, right = neighbors.split(",")
        left_dict[node] = left
        right_dict[node] = right
    return left_dict, right_dict


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()

    instructions = list(input[0].strip())
    go_left, go_right = input_to_dicts(input[2::])

    # Puzzle 1
    steps = get_steps(
        go_left=go_left,
        go_right=go_right,
        start="AAA",
        end="ZZZ",
        instructions=instructions,
    )

    print(f"Puzzle 1: number of steps is {steps}")

    # Puzzle 2
    start_locations = np.array(
        [location for location in go_left.keys() if location[-1] == "A"]
    )

    steps_to_z = [
        get_steps(
            go_left=go_left,
            go_right=go_right,
            start=start,
            end="Z",
            instructions=instructions,
        )
        for start in start_locations
    ]
    steps = np.lcm.reduce(np.array(steps_to_z, dtype=np.int64))
    print(f"\nPuzzle 2: number of steps is {steps}")


if __name__ == "__main__":
    main("input.txt")
