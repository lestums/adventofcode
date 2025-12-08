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
            line = list(filter(None, line.strip().split(" ")))
            if not line:
                continue
            result.append(line)
    result = list(map(list, zip(*result)))
    return result

def compute_problems_one(operation, logger):
    math_op = operation[-1]
    accumulator = 0

    for integer in operation[:len(operation) -1]:
        value = int(integer)
        logger.debug(f"Operation: {math_op}, Value: {value}, Accumulator: {accumulator}")
        if math_op == "+":
            accumulator += value
        if math_op == "*":
            if accumulator == 0:
                accumulator = 1
            accumulator *= value
        if math_op == "-":
            accumulator -= value

    return accumulator

def compute_problems_two(operation, logger):
    math_op = operation[-1]
    accumulator = 0

    operation = operation[:len(operation) -1]
    max_len = max(len(x) for x in operation)
    operation = [x.rjust(max_len) for x in operation]

    result = []

    print(operation)

    # Process each column from right to left
    for col in range(max_len - 1, -1, -1):
        digits = []
        for row in operation:
            if row[col] == ' ':
                continue
            else:
                digits.append(row[col])
        result.append(int("".join(digits)))

    print(result)

    for integer in result:
        value = int(integer)
        logger.debug(f"Operation: {math_op}, Value: {value}, Accumulator: {accumulator}")
        if math_op == "+":
            accumulator += value
        if math_op == "*":
            if accumulator == 0:
                accumulator = 1
            accumulator *= value
        if math_op == "-":
            accumulator -= value

    return accumulator

def solve_trash(fn, ops, logger):
    compute_fn = partial(fn, logger=logger)
    with mp.Pool() as pool:
        problems = pool.map(compute_fn, ops)

    return sum(problems)

def solve_trash_one(ops, logger):
    return solve_trash(compute_problems_one, ops, logger)

def solve_trash_two(ops, logger):
    return solve_trash(compute_problems_two, ops, logger)

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

    ops = read_file(args.input_file)

    logger.debug(ops)

    logger.info(f"Total of problems for round 1 : {solve_trash_one(ops, logger)}")
    logger.info(f"Total of problems for round 2 : {solve_trash_two(ops, logger)}")

if __name__ == "__main__":
    main()
