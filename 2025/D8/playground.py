#!/usr/bin/env python3

import argparse
import sys
import multiprocessing as mp

from collections import Counter
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
    result = []
    with open(path, "r") as f:
        for line in f:
            box = [int(coordinate) for coordinate in line.strip().split(",")]
            if not line:
                continue
            result.append(box)
    return result

def solve_junctionboxes_one(junctionbox_map, logger):
    return 0

def solve_junctionboxes_two(junctionbox_map, logger):
    return 0

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

    junctionbox_map = read_file(args.input_file)

    logger.debug(junctionbox_map)

    logger.info(f"Size of circuits for round 1 : {solve_junctionboxes_one(junctionbox_map, logger)}")
    logger.info(f"Size of circuits for round 2 : {solve_junctionboxes_two(junctionbox_map, logger)}")

if __name__ == "__main__":
    main()
