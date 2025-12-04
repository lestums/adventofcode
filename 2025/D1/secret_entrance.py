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
            result.append(line)
    return result

def solve_secretentrance_one(rotary_sequence, logger):
    mod = 100
    dial_pointer = 50
    password = 0

    for sequence in rotary_sequence:
        direction = sequence[0]
        value = int(sequence[1:])

        if direction == "L":
            value = mod - value

        logger.debug(f"Start: {dial_pointer}, direction value: {value}")
        dial_pointer = (dial_pointer + value) % (mod)

        if dial_pointer == 0:
            password += 1

        logger.debug(f"dial is now at {dial_pointer}. Password value: {password}")

    return password

def solve_secretentrance_two(rotary_sequence, logger):
    mod = 100
    dial_pointer = 50
    password = 0

    for sequence in rotary_sequence:
        direction = sequence[0]
        value = int(sequence[1:])
        old_dial_ptr = dial_pointer

        if direction == "L":
            dial_pointer -= value
        if direction == "R":
            dial_pointer += value

        old_hundred = old_dial_ptr // 100
        current_hundred = dial_pointer // 100

        diff = abs(current_hundred - old_hundred)
        password += diff

        if direction == "L":
            if dial_pointer % mod == 0:
                password += 1
            if old_dial_ptr % mod == 0:
                password -= 1

        logger.debug(f"dial is now at {dial_pointer}. Password value: {password}")

    return password

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

    rotary_sequence = read_file(args.input_file)

    logger.info(rotary_sequence)

    logger.info(f"Password for round 1 : {solve_secretentrance_one(rotary_sequence, logger)}")
    logger.info(f"Password for round 2 : {solve_secretentrance_two(rotary_sequence, logger)}")

if __name__ == "__main__":
    main()
