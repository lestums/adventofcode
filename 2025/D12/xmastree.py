#!/usr/bin/env python3

import argparse
import itertools
import sys
import networkit as nk
import matplotlib.pyplot as plot

from datetime import datetime
from functools import lru_cache

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
    result = { "shapes" : [], "regions" : []}
    max_row = 0
    max_col = 0
    shape = []
    is_shape = False
    is_region = False
    shape_number = 0
    with open(path, "r") as f:
        for line in f:
            if ":" in line and "x" not in line:
                is_shape = True
                continue
            if "x" in line and ":" in line:
                is_shape = False
                is_region = True
            if not line or not line.strip():
                if is_shape:
                    result["shapes"].append((sum(line.count("#") for line in shape), shape))
                    shape = []
                    shape_number += 1
                    is_shape = False
                is_region = False
                continue
            if is_shape:
                shape.append(line.strip())
            if is_region:
                region = line.strip().split(":")
                region_x = int(region[0].split("x")[0])
                region_y = int(region[0].split("x")[1])
                region_S = region_x * region_y
                result["regions"].append((region_x, region_y, region_S,region[1].strip().split(" ")))
    return result

def evaluate_region(region, shapes, logger):
    region_x = region[0]
    region_y = region[1]
    region_area = region[2]

    total_area = 0
    num_shapes = 0

    for shape_index, count in enumerate(region[3]):
        total_area += (int(count) * int(shapes[shape_index][0]))
        num_shapes += int(count)

    # Not possible if the shapes takes more space than the available area
    if total_area > region_area:
        return False

    possible_shapes = (region_x / 3) * (region_y / 3)

    # Possible if the shapes area is lesser or equal as the number of shapes
    if possible_shapes >= num_shapes:
        return True

    # Monkey smashing keyboard again... ASDKJASDJASKLDJSAKDJAKLDJKALSJDKASDJ !
    return False

def solve_tetris_one(tetris, logger):
    total = 0

    # Monkey it, but smart
    for region in tetris["regions"]:
        logger.debug(f"Evaluating region: {region}")
        if evaluate_region(region, tetris["shapes"], logger):
            total += 1

    return total

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

    tetris = read_file(args.input_file)

    logger.debug(tetris)

    logger.info(f"Total of regions fitting for round 1 : {solve_tetris_one(tetris, logger)}")
    logger.info(f"Free star for round 2 \\o/")

if __name__ == "__main__":
    main()
