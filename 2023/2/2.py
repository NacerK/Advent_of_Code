import re
import pandas as pd


def input_to_df(input: list[str]) -> pd.DataFrame:
    """parse the whole input string of game data and returns a dataframe with the id of
    the game, max number of drawn cubes for red, green and blue colors
    """
    data = []
    for line in input:
        game_x, sets = line.split(":")
        data.append(
            {
                "id": int(game_x.split(" ")[1]),
                "red": max([int(x) for x in re.findall(r"(\d+)\sred", sets)]),
                "green": max([int(x) for x in re.findall(r"(\d+)\sgreen", sets)]),
                "blue": max([int(x) for x in re.findall(r"(\d+)\sblue", sets)]),
            }
        )

    return pd.DataFrame(data)


def main(input_path: str):
    # read input
    with open(input_path, "r") as f:
        input = f.readlines()
    # extract the input's relevant info to a dataframe
    df = input_to_df(input)
    # compute the power of each game
    df["power"] = df["red"] * df["green"] * df["blue"]
    # get the ids of possible games
    max_red, max_green, max_blue = 12, 13, 14
    possible_games_mask = (
        (df.red <= max_red) * (df.blue <= max_blue) * (df.green <= max_green)
    )
    possible_games_ids = df[possible_games_mask]["id"]

    print(
        f"Puzzle 1 answer: The sum of the possible games ids "
        f"is: {possible_games_ids.sum()}"
    )
    print(
        f"Puzzle 2 answer: The sum of the powers of all games is: {df['power'].sum()}"
    )


if __name__ == "__main__":
    main("input1.txt")
