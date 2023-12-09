import pandas as pd


def input_to_df(input: list[str]) -> pd.DataFrame:
    """load the input into a dataframe"""

    data = {"wining": [], "scratched": []}

    for line in input:
        numbers = line.rstrip().split(":")[1].split("|")
        data["wining"].append({int(n) for n in numbers[0].split()})
        data["scratched"].append({int(n) for n in numbers[1].split()})

    return pd.DataFrame(data)


def intersect_row(row):
    return row["wining"].intersection(row["scratched"])


def get_worth(row):
    return 0 if row["correct_scratches"] == 0 else pow(2, row["correct_scratches"] - 1)


def get_total_won_copies(df: pd.DataFrame, card_number: int):
    """get total number of won copies of a specific card number"""
    won_copies_numbers = list(
        range(
            card_number + 1,
            card_number + 1 + df.loc[card_number]["correct_scratches"],
        )
    )
    total_won_copies = 0
    for won_copie_number in won_copies_numbers:
        if won_copie_number not in df.index:
            continue
        else:
            total_won_copies += 1 + df.loc[won_copie_number]["total_won_copies"]

    return total_won_copies


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()

    # load input to dataframe
    df = input_to_df(input)
    # find the intersection between scratched and winning numbers for each card
    df["intersection"] = df.apply(intersect_row, axis=1)
    # compute the number of intersection elements
    df["correct_scratches"] = df["intersection"].apply(lambda x: len(x))
    # compute the worth of each card
    df["worth"] = df.apply(get_worth, axis=1)

    print(f"Puzzle 1: Total worth is {df['worth'].sum()} ")

    # Puzzle 2
    # initialize the total number of copies won by each card
    df["total_won_copies"] = 0
    # compute the total number of copies won by each card starting from the last cards
    for card_number, row in df[::-1].iterrows():
        df.at[card_number, "total_won_copies"] = get_total_won_copies(df, card_number)
    # number of original cards + sum of all won copies
    total_cards = len(df) + sum(df["total_won_copies"])

    print(f"Puzzle 2: Total number of cards is {total_cards} ")
    # print(df[["correct_scratches", "total_won_copies"]].to_string())


if __name__ == "__main__":
    main("input.txt")
