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
    result = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            idranges = line.split(',')
            result += idranges
    return result

def has_sequences_twice(id_val):
    id_str = str(id_val)

    if len(id_str) % 2 != 0:
        return None

    half = len(id_str) // 2
    part = id_str[:half]

    if part * 2 == id_str:
        return part

    return None

def has_sequences_twice_more(id_val):
    id_str = str(id_val)

    for size in range(1, len(id_str) // 2 + 1):
        if len(id_str) % size == 0:
            part = id_str[:size]
            repetitions = len(id_str) // size

            if part * repetitions == id_str and repetitions >= 2:
                return part

    return None

def get_invalid_ids_in_range(idrange, sequence_fn, logger):
    logger.debug(f"Range is : {idrange}")

    invalid_ids = [ ]

    range_start = int(idrange.split('-')[0])
    range_end = int(idrange.split('-')[1])

    for id_val in range(range_start, range_end + 1):
        if sequence_fn(id_val) is not None:
            invalid_ids.append(id_val)
            logger.debug(f"Invalid ids list: {invalid_ids}")

    return sum(invalid_ids)

def solve_giftshop(fn, idranges, sequence_fn, logger):
    compute_fn = partial(fn, logger=logger, sequence_fn=sequence_fn)
    with mp.Pool() as pool:
        invalid_ids = pool.map(compute_fn, idranges)

    return sum(invalid_ids)

def solve_giftshop_one(idranges, logger):
    return solve_giftshop(get_invalid_ids_in_range, idranges, has_sequences_twice, logger)

def solve_giftshop_two(idranges, logger):
    return solve_giftshop(get_invalid_ids_in_range, idranges, has_sequences_twice_more, logger)

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

    idranges = read_file(args.input_file)

    logger.info(idranges)

    logger.info(f"Sum of invalid ids for round 1 : {solve_giftshop_one(idranges, logger)}")
    logger.info(f"Sum of invalid ids for round 2 : {solve_giftshop_two(idranges, logger)}")

if __name__ == "__main__":
    main()
