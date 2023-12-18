import networkx as nx
import numpy as np

from itertools import combinations


def expand_universe(input_np: np.ndarray) -> np.ndarray:
    input_exp = input_np.copy()
    # mask = true where there is no #, false where there is #
    mask = ~np.isin(input_np, "#")
    per_col_mask = mask.all(axis=0)
    per_row_mask = mask.all(axis=1)
    # index of columns and rows to expand
    col_to_expand = np.where(per_col_mask)[0]
    row_to_expand = np.where(per_row_mask)[0]
    # columns and lines to insert
    col_to_insert = np.array([["*"] for i in range(input_np.shape[0])])
    row_to_insert = ["*" for i in range(input_np.shape[1] + col_to_expand.shape[0])]
    # expand columns and rows
    input_exp = np.insert(input_exp, col_to_expand, col_to_insert, axis=1)
    input_exp = np.insert(input_exp, row_to_expand, row_to_insert, axis=0)

    return input_exp


def np_to_graph(input_np: np.ndarray, gap_value: int = 1) -> nx.Graph:
    graph = nx.Graph()

    for i in range(input_np.shape[0]):
        for j in range(input_np.shape[1]):
            graph.add_node(f"{i}.{j}")
            weight = gap_value if input_np[i, j] == "*" else 1

            if i != input_np.shape[0] - 1:
                graph.add_edge(f"{i}.{j}", f"{i+1}.{j}", weight=weight)
            if j != input_np.shape[1] - 1:
                graph.add_edge(f"{i}.{j}", f"{i}.{j+1}", weight=weight)

    return graph


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()

    input_np = np.array([list(line.strip()) for line in input])
    input_exp = expand_universe(input_np)
    graph = np_to_graph(input_exp, gap_value=1)

    # get all combinations of pairs of galaxies
    gal_nodes = [
        f"{idx[0]}.{idx[1]}"
        for idx in zip(np.where(input_exp == "#")[0], np.where(input_exp == "#")[1])
    ]
    gal_nodes_combinations = list(combinations(gal_nodes, 2))

    # compute the shortest path between each combination and sum them
    shortest_paths_sum = 0

    for comb in gal_nodes_combinations:
        shortest_paths_sum += nx.dijkstra_path_length(
            graph, comb[0], comb[1], weight="weight"
        )

    print(f"Puzzle 1: sum of shortest paths is {shortest_paths_sum}")

    # Puzzle 2
    graph_p2 = np_to_graph(input_exp, gap_value=999999)
    shortest_paths_sum_2 = 0

    for comb in gal_nodes_combinations:
        shortest_paths_sum_2 += nx.dijkstra_path_length(
            graph_p2, comb[0], comb[1], weight="weight"
        )
    print(f"Puzzle 2: sum of shortest paths is {shortest_paths_sum_2}")


if __name__ == "__main__":
    main("input.txt")
