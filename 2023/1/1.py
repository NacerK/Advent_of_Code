import regex as re

# a dict that maps string digits as english words or numerical digits to int
digit_str_to_int = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
} | {str(i): i for i in range(1, 10)}


def extract_digits(x: str) -> list[int]:
    """Extract a list of digits from a string "x" in their order of appearance"""

    # note: it took me a while to figure out that there might be overlapped cases (e.g. oneight)
    # setting overlapped to True did the trick
    return re.compile(r"|".join(digit_str_to_int.keys())).findall(x, overlapped=True)


def get_calibration_values(input_string: list[str]) -> list[int]:
    calibration_values = []
    # process each line individually
    for line in input_string:
        digits = extract_digits(line)
        calibration_values.append(
            int(f"{digit_str_to_int[digits[0]]}{digit_str_to_int[digits[-1]]}")
        )
    return calibration_values


if __name__ == "__main__":
    # load input
    with open("input.txt", "r") as f:
        input1_string = f.readlines()
    # process input
    calibration_values = get_calibration_values(input1_string)
    print(f"Input calibration values sum is {sum(calibration_values)}")
