#!/usr/bin/env python3

import argparse
import sys
import multiprocessing as mp

from datetime import datetime
from functools import partial

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
    fresh_ranges = []
    ingredient_ids = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                break
            fresh_ranges.append((int(line.split("-")[0]), int(line.split("-")[1])))
        for line in f:
            line = line.strip()
            if not line:
                continue
            ingredient_ids.append(int(line))
    return fresh_ranges, ingredient_ids

def solve_cafeteria_one(ingredient_ids, fresh_ranges, logger):
    fresh = 0

    for ingredient_id in ingredient_ids:
        for fresh_range in fresh_ranges:
            left_bound = fresh_range[0]
            right_bound = fresh_range[1]

            if ingredient_id > right_bound:
                logger.debug(f"Ingredient ID {ingredient_id} : skip to next range")
                continue

            if ingredient_id >= left_bound and ingredient_id <= right_bound:
                logger.debug(f"Ingredient ID {ingredient_id} is fresh !")
                fresh +=1
                break

    return fresh

def merge_ranges(ranges):
    ranges = sorted(ranges, key=lambda x: x[0])
    merged = [ranges[0]]

    for current_start, current_end in ranges[1:]:
        last_start, last_end = merged[-1]

        if current_start <= last_end:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged

def solve_cafeteria_two(ingredient_ids, fresh_ranges, logger):
    count = 0

    new_ranges = merge_ranges(fresh_ranges)

    for fresh_range in new_ranges:
        num = len(range(fresh_range[0], fresh_range[1] + 1))
        logger.debug(f"There are {num} valid ingredient IDs in range {fresh_range}")
        count += num

    return count

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

    fresh_ranges, ingredient_ids = read_file(args.input_file)

    logger.debug(fresh_ranges)
    logger.debug(ingredient_ids)

    logger.info(f"Total of fresh ingredient IDs for round 1 : {solve_cafeteria_one(ingredient_ids, fresh_ranges, logger)}")
    logger.info(f"Total of fresh ingredient IDs for round 2 : {solve_cafeteria_two(ingredient_ids, fresh_ranges, logger)}")

if __name__ == "__main__":
    main()
