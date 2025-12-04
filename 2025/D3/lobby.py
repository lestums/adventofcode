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
            digits = [int(ch) for ch in line]
            result.append(digits)
    return result

def get_max_joltage_in_battery(battery, logger):
    count = 1
    max_joltage = 0
    max_tenth = 0

    logger.debug(f"Battery is : {battery}")

    for i in battery:
        # Do not waste time if the next number for tenth is
        # less than the previous iteration
        if i < max_tenth:
            continue
        # End is here
        if count == len(battery):
            break
        for j in battery[count:]:
            current_joltage = i * 10 + j
            logger.debug(f"{current_joltage} > {max_joltage}")
            if current_joltage > max_joltage:
                max_joltage = current_joltage
                logger.debug(f"max_joltage is now: {max_joltage}")

        count += 1

    return max_joltage

def get_max_joltage_in_battery_12d(battery, logger):
    if len(battery) < 12:
        raise ValueError("Array must contain at least 12 integers.")

    result = []
    start = 0

    for remaining in range(12, 0, -1):
        end = len(battery) - remaining

        max_digit = max(battery[start : end + 1])

        for i in range(start, end + 1):
            if battery[i] == max_digit:
                result.append(max_digit)
                start = i + 1
                break

    max_joltage = int("".join(str(d) for d in result))

    logger.debug(f"max_joltage is now: {max_joltage}")

    return max_joltage


def solve_lobby(fn, batteries, logger):
    compute_fn = partial(fn, logger=logger)
    with mp.Pool() as pool:
        joltages = pool.map(compute_fn, batteries)

    return sum(joltages)

def solve_lobby_one(batteries, logger):
    return solve_lobby(get_max_joltage_in_battery, batteries, logger)

def solve_lobby_two(batteries, logger):
    return solve_lobby(get_max_joltage_in_battery_12d, batteries, logger)

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

    batteries = read_file(args.input_file)

    logger.info(f"Max joltage for round 1 : {solve_lobby_one(batteries, logger)}")
    logger.info(f"Max joltage for round 2 : {solve_lobby_two(batteries, logger)}")

if __name__ == "__main__":
    main()
