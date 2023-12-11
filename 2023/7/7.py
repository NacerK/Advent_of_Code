from string import ascii_lowercase
import pandas as pd
import numpy as np

puzzle1_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
puzzle2_order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def use_joker(row):
    unique_cards, unique_counts = np.unique(
        np.array(list(row.replace("J", ""))), return_counts=True
    )
    # not empty (it means we have other cards than J)
    if unique_cards.size:
        # replace J with the most recurrent card
        return row.replace("J", unique_cards[unique_counts.argmax()])
    else:
        return row


def get_hand_strenght(row) -> int:
    unique_counts = np.unique(np.array(list(row)), return_counts=True)[1]
    return unique_counts.max() - len(unique_counts)


def get_cards_strength(row, card_order: list[str]) -> str:
    """Card strength is identified by a letter ranging from 'a' to 'n', 'a' being the
    strongest"""
    strenght_mapping = {card: ascii_lowercase[i] for i, card in enumerate(card_order)}
    return "".join([strenght_mapping[card] for card in row])


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()

    hands = np.array([line.split()[0] for line in input])
    bids = np.array([line.split()[1] for line in input], dtype=int)

    df = pd.DataFrame({"hand": hands, "bid": bids})

    df["hand_strength"] = df["hand"].apply(get_hand_strenght)
    df["card_strength"] = df["hand"].apply(
        lambda x: get_cards_strength(x, puzzle1_order)
    )
    # sort from strongest to weakest
    df = df.sort_values(["hand_strength", "card_strength"], ascending=[False, True])
    df["rank"] = range(len(df), 0, -1)
    df["winning"] = df["bid"] * df["rank"]

    print(f"Puzzle 1: total winnings are {df['winning'].sum()}")

    # Puzzle 2
    df["hand_post_joker"] = df["hand"].apply(use_joker)
    df["hand_strength"] = df["hand_post_joker"].apply(get_hand_strenght)
    df["card_strength"] = df["hand"].apply(
        lambda x: get_cards_strength(x, puzzle2_order)
    )
    # sort from strongest to weakest
    df = df.sort_values(["hand_strength", "card_strength"], ascending=[False, True])
    df["rank"] = range(len(df), 0, -1)
    df["winning"] = df["bid"] * df["rank"]

    print(f"Puzzle 2: total winnings are {df['winning'].sum()}")


if __name__ == "__main__":
    main("input.txt")
