import numpy as np


def predict_next_point(l: np.ndarray) -> int:
    l_new = np.diff(l)
    if (l_new == 0).all():
        return l_new[-1] + l[-1]
    else:
        return l[-1] + predict_next_point(l_new)


def predict_previous_point(l: np.ndarray) -> int:
    l_new = np.diff(l)
    if (l_new == 0).all():
        return l[0] - l_new[0]
    else:
        return l[0] - predict_previous_point(l_new)


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()

    input_np = np.array([[int(e) for e in line.split()] for line in input])

    predictions = [predict_next_point(input_np[i]) for i in range(input_np.shape[0])]

    print(f"Puzzle 1: the sum of all predictions is {sum(predictions)}")
    # part two
    predictons_p2 = [
        predict_previous_point(input_np[i]) for i in range(input_np.shape[0])
    ]
    print(f"Puzzle 2: the sum of all predictions is {sum(predictons_p2)}")


if __name__ == "__main__":
    main("input.txt")
