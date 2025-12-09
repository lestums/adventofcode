#!/usr/bin/env python3

import argparse
import sys
import numpy as np

from collections import defaultdict
from datetime import datetime

class Logger:
    def __init__(self, debug=False):
        self.debug_enabled = debug

    def _log(self, level, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stderr.write(f"[{timestamp}] [{level}] {msg}\n")

    def debug(self, msg):
        if self.debug_enabled:
            self._log("DEBUG", msg)

    def info(self, msg):
        self._log("INFO", msg)

    def warning(self, msg):
        self._log("WARNING", msg)

    def error(self, msg):
        self._log("ERROR", msg)

def read_file(path):
    result = []
    max_row = 0
    max_col = 0
    with open(path, "r") as f:
        for line in f:
            coordinates = tuple(line.strip().split(","))
            max_row = max(int(coordinates[0]), max_row)
            max_col = max(int(coordinates[1]), max_col)
            if not line:
                continue
            result.append(coordinates)
    return result, max_row, max_col

def print_square(one, two, three, four):
    one_x = one[0]
    one_y = one[1]
    two_x = two[0]
    two_y = two[1]
    three_x  = three[0]
    three_y = three[1]
    four_x = four[0]
    four_y = four[1]

    size_x = max(one_x, two_x, three_x, four_x) + 2
    size_y = max(one_y, two_y, three_y, four_y) + 2

    grid = np.full((size_y, size_x), ".")

    grid[one_y][one_x] = "1"
    grid[two_y][two_x] = "2"
    grid[three_y][three_x] = "3"
    grid[four_y][four_x] = "4"

    print(grid)
    print()

def print_updated_tile_map(grid, one, two, three, four):
    one_x = one[0]
    one_y = one[1]
    two_x = two[0]
    two_y = two[1]
    three_x  = three[0]
    three_y = three[1]
    four_x = four[0]
    four_y = four[1]

    grid[one_y][one_x] = "1"
    grid[two_y][two_x] = "2"
    grid[three_y][three_x] = "3"
    grid[four_y][four_x] = "4"

    print(grid)
    print()

def print_tile_map(tile_map):
    tiles = tile_map[0]
    rows = tile_map[1] + 2
    cols = tile_map[2] + 2

    grid = np.full((cols, rows), ".")

    for tile in tiles:
        row = int(tile[0])
        col = int(tile[1])
        tile = tile[2]

        if tile == "red":
            grid[col][row] = "#"
        if tile == "green":
            grid[col][row] = "X"

    return grid

def solve_rectangle_one(tile_map, logger):
    red_tiles = tile_map[0]
    max_row = tile_map[1]
    max_col = tile_map[2]

    rectangle_areas = []

    # Find biggest rectangles
    for (index, tile) in enumerate(red_tiles):
        row = int(tile[0])
        col = int(tile[1])

        for next_tile in red_tiles[index:]:
            next_row = int(next_tile[0])
            next_col = int(next_tile[1])

            if row == next_row and col == next_col:
                continue

            area = max(abs(col - next_col + 1), 1) * max(abs(row - next_row + 1), 1)
            logger.debug(f"Corner 1: {row},{col}; Corner 2: {next_row},{next_col}; Area: {area}")
            rectangle_areas.append(area)

    return max(rectangle_areas)

def solve_rectangle_two(tile_map, logger):
    red_tiles = tile_map[0]
    max_row = tile_map[1]
    max_col = tile_map[2]

    rectangle_areas = []

    all_tiles = set()

    # Generate green tiles
    for (index, tile) in enumerate(red_tiles):
        row = int(tile[0])
        col = int(tile[1])

        all_tiles.add((row, col, "red"))

        for next_tile in red_tiles[index:]:
            next_row = int(next_tile[0])
            next_col = int(next_tile[1])

            if row != next_row and col != next_col:
                continue

            if row == next_row:
                start = min(col, next_col)
                finish = max(col, next_col)

                while start < finish:
                    all_tiles.add((row, start, "green"))
                    start += 1

            if col == next_col:
                start = min(row, next_row)
                finish = max(row, next_row)

                while start < finish:
                    all_tiles.add((start, col, "green"))
                    start += 1

    rows = defaultdict(list)
    cols = defaultdict(list)
    result = set()

    for x, y, t in all_tiles:
        rows[x].append((y,t))
        cols[y].append((x,t))

    # Fill horizontal gaps
    for x, ys in rows.items():
        ys = sorted(ys)
        for i in range(len(ys) - 1):
            start, end = ys[i][0], ys[i+1][0]
            result.add((x, start, ys[i][0]))
            result.add((x, end, ys[i+1][0]))

            for y in range(start, end + 1):
                result.add((x, y, "green"))

    # Fill vertical gaps
    for y, xs in cols.items():
        xs = sorted(xs)
        for i in range(len(xs) - 1):
            start, end = xs[i][0], xs[i+1][0]
            for x in range(start, end + 1):
                result.add((x, y, "green"))

    for tile in all_tiles:
        if tile[2] == "red":
            result.remove((tile[0],tile[1],"green"))
            result.add(tile)

    # Find biggest rectangles
    for (index, tile) in enumerate(result):
        row = int(tile[0])
        col = int(tile[1])
        tile_type = tile[2]

        if tile_type != "red":
            continue

        third = (0, 0, tile_type)
        fourth = (0, 0, tile_type)

        for next_tile in result:
            if tile == next_tile:
                continue
            next_row = int(next_tile[0])
            next_col = int(next_tile[1])

            if row == next_row or col == next_col:
                continue

            diff_col = abs(col - next_col + 1)

            if row > next_row:
                diff_row = row - next_row + 1
                third = (row, next_col, "red")
                fourth = (next_row, col, "red")
            else:
                diff_row = next_row - row + 1
                third = (next_row, col, "red")
                fourth = (row, next_col, "red")

            area = diff_row * diff_col
            if third not in all_tiles or fourth not in all_tiles:
                continue

            rectangle_areas.append(area)

    return max(rectangle_areas)

def main():
    parser = argparse.ArgumentParser(description="Read file and split each line into digits.")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug output"
    )

    args = parser.parse_args()

    logger = Logger(debug=args.debug)

    tile_map = read_file(args.input_file)

    logger.debug(tile_map)

    logger.info(f"Max rectangle area for round 1 : {solve_rectangle_one(tile_map, logger)}")
    logger.info(f"Max rectangle area for round 2 : {solve_rectangle_two(tile_map, logger)}")

if __name__ == "__main__":
    main()
