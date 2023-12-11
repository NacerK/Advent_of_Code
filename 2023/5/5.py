import re

import tqdm
import numpy as np


def get_destinations(
    map_values: list[str], initial_sources: np.ndarray, n_batches: int = 50
) -> np.ndarray:
    """get destinations of a list of initial_sources using map values"""

    destinations = initial_sources

    # load mapping values into a np array of int elements
    map_values_int = np.array(
        [
            [int(x) for x in line.strip().split()]
            for line in map_values
            if len(line) > 1
        ],
        dtype=np.int64,
    )
    # process initial seeds as 10 batches to avoid numpy memory limitations
    batch_size = len(destinations) // n_batches
    for i in tqdm.tqdm(range(n_batches)):
        batch = (
            destinations[i * batch_size : (i + 1) * batch_size]
            if i != n_batches - 1
            else destinations[i * batch_size :]
        )
        #  mask of mapping of each source, with shape [n_sources , n_mapping]
        source_mapping_mask = (batch[:, None] >= map_values_int[:, 1]) & (
            batch[:, None] < map_values_int[:, 1] + map_values_int[:, 2]
        )
        mapped_sources_ids, mapping_ids = np.where(source_mapping_mask)
        batch[mapped_sources_ids] = (
            map_values_int[mapping_ids, 0]
            + batch[mapped_sources_ids]
            - map_values_int[mapping_ids, 1]
        )

    return destinations


def input_to_localisations(input: str, initial_seeds: np.ndarray) -> np.ndarray:
    """Get localisations from the input string containing the mappings and a list of
    initial seeds"""

    # get all map names and values with a regex
    map_pattern = re.compile(r"(.*map:\s*)\n([\s\S]+?)(?=\n\w+-to|$)")
    maps = map_pattern.findall(input)

    init_sources = initial_seeds
    # load each map into a df
    for map_name, map_values in tqdm.tqdm(maps):
        source_name, _, dest_name = map_name.split()[0].split("-")
        init_sources = get_destinations(map_values.split("\n"), init_sources)

    return init_sources


def main(input_path: str):
    with open(input_path, "r") as f:
        input = f.read()

    initial_seeds = np.array(
        [int(seed) for seed in input.split("\n")[0].split(":")[1].split()],
        dtype=np.int64,
    )
    localisations = input_to_localisations(input, initial_seeds)

    print(f"Puzzle 1: The lowest location is: " f"{localisations.min()}")

    # Puzzle two
    initial_seeds = np.array(
        [int(seed) for seed in input.split("\n")[0].split(":")[1].split()],
        dtype=np.int64,
    )

    it = iter(initial_seeds)
    initial_seeds_p2 = np.ndarray(sum([b for a, b in zip(it, it)]), dtype=np.int64)
    it = iter(initial_seeds)
    i = 0

    for init_seed, range_size in tqdm.tqdm(zip(it, it)):
        initial_seeds_p2[np.arange(i, i + range_size)] = np.arange(
            init_seed, init_seed + range_size
        )
        i += range_size

    localisations = input_to_localisations(input, initial_seeds_p2)
    print(f"Puzzle 2: The lowest location is: " f"{localisations.min()}")


if __name__ == "__main__":
    main("input.txt")
