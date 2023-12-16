from operator import add
import numpy as np
import networkx as nx

import shapely.geometry as sg
from shapely.prepared import prep

move_clockwise = {
    "|": (-1, 0),
    "-": (0, 1),
    "L": (0, 1),
    "J": (0, -1),
    "7": (1, 0),
    "F": (0, 1),
    ".": (0, 0),
}
move_anticlockwise = {
    "|": (1, 0),
    "-": (0, -1),
    "L": (-1, 0),
    "J": (-1, 0),
    "7": (0, -1),
    "F": (1, 0),
    ".": (0, 0),
}


def input_to_graph(
    input: list[str], start_direction: tuple[int, int]
) -> tuple[nx.Graph, np.ndarray]:
    input_np = np.array([[elem for elem in line.strip()] for line in input])
    # list of nodes and edges to use to create a nx.Graph
    nodes = []
    edges = []
    # we find te starting position (S)
    start = [dim[0] for dim in np.where(input_np == "S")]
    nodes.append("S")
    # array storing the positions of loop elements
    positions = [(start[0], start[1])]
    # for my input, this is where to go to start a clockwise movement from S
    previous_position = start
    position = [start[0] + start_direction[0], start[1] + start_direction[1]]

    while True:
        char = input_np[position[0], position[1]]
        positions.append((position[0], position[1]))
        if char == "S":
            # we link the last node of the loop to S
            edges.append((nodes[-1], nodes[0]))
            break
        # nodes are named with their character and their x,y coordinates
        node = f"{char}.{position[0]}.{position[1]}"
        edges.append((nodes[-1], node))
        nodes.append(node)
        # move to next connected pipe
        if list(map(add, position, move_clockwise[char])) != previous_position:
            previous_position = position
            position = list(map(add, position, move_clockwise[char]))
        else:
            previous_position = position
            position = list(map(add, position, move_anticlockwise[char]))

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    return graph.to_undirected(), np.array(positions)


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.readlines()

    graph, positions = input_to_graph(input, start_direction=(-1, 0))
    distance_dict = nx.single_source_dijkstra_path(graph, "S")
    farthest_steps = max([len(nodes) for nodes in distance_dict.values()]) - 1

    print(f"Puzzle 1: number of steps to farthest point is {farthest_steps}")

    # Puzzle 2
    points_to_check = np.array(
        [(i, j) for i in range(len(input)) for j in range(len(input[0]) - 1)]
    )

    # with shapely
    polygon = sg.Polygon(positions)
    prep_polygon = prep(polygon)
    points_inside_polygon = [
        prep_polygon.contains(sg.Point(point)) for point in points_to_check
    ]

    print(f"Puzzle 2 shapely: number of enclosed tiles is {sum(points_inside_polygon)}")


if __name__ == "__main__":
    main("input.txt")
