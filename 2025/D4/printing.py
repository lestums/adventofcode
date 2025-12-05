#!/usr/bin/env python3

import argparse
import sys
import numpy as np

from datetime import datetime
from functools import partial
from scipy.signal import convolve2d

neighbors = np.array([
    [ True, True, True ],
    [ True, False, True ],
    [ True, True, True ]
])

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
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            roll_line = np.array([c == "@" for c in line])
            result.append(roll_line)
    return np.array(result)

def solve_printing_one(rolls, logger):
    convolute_neighbor = convolve2d(rolls.astype(int), neighbors, mode="same")
    forklift_operation = (convolute_neighbor <= 3) & rolls
    rolls = rolls & (~forklift_operation)
    return rolls, forklift_operation.sum()

def solve_printing_two(rolls, logger):
    # Do a first pass
    results = solve_printing_one(rolls, logger)
    current_rolls = results[0]
    total = results[1]

    removed = total
    while removed > 0:
        results = solve_printing_one(current_rolls, logger)
        current_rolls = results[0]
        removed = results[1]
        total += removed
        logger.debug(f"Roll of paper removed: {removed}; Total: {total}")

    return current_rolls, total

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

    rolls = read_file(args.input_file)

    logger.debug(rolls)

    logger.info(f"Num of paper roll for round 1 : {solve_printing_one(rolls, logger)[1]}")
    logger.info(f"Num of paper roll for round 2 : {solve_printing_two(rolls, logger)[1]}")

if __name__ == "__main__":
    main()
