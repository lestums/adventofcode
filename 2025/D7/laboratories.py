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
            line = line.strip()
            if not line:
                continue
            result.append(line)
    return result

def manifold_print(manifold):
    for line in manifold:
        print(line)

def solve_tachyon_one(manifold, logger):
    source_line = manifold[0]
    source_pos = source_line.find('S')
    total_splits = 0
    beams = set()
    new_beams = set()
    output_manifold = manifold

    # Split all beams
    for line in range(1, len(manifold)):
        manifold_line = list(manifold[line])

        # If no new beams, just propagate from source
        if not new_beams:
            manifold_line[source_pos] = "|"
            output_manifold[line] = "".join(manifold_line)
            new_beams.add(source_pos)
            continue

        beams = new_beams.copy()

        for beam in beams:
            # Splitter !
            if manifold_line[beam] == "^":
                manifold_line[beam - 1] = "|"
                manifold_line[beam + 1] = "|"
                output_manifold[line] = "".join(manifold_line)
                new_beams.remove(beam)
                new_beams.add(beam - 1)
                new_beams.add(beam + 1)
                total_splits += 1
                continue

            # No splitter, just repeat
            manifold_line[beam] = "|"
            output_manifold[line] = "".join(manifold_line)

        logger.debug(f"Beam list : {beams}")

    manifold_print(output_manifold)

    return output_manifold, total_splits

def solve_tachyon_two(manifold, logger):
    possible_paths = Counter()
    for manifold_line in manifold:
        for index in range (0, len(manifold_line)):
            char = list(manifold_line)[index]
            if char == 'S':
                possible_paths[index] = 1
            if char == '^':
                if index in possible_paths:
                    possible_paths[index-1] += possible_paths[index]
                    possible_paths[index+1] += possible_paths[index]
                    del possible_paths[index]

    return possible_paths.total()

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

    manifold = read_file(args.input_file)

    logger.debug(manifold)

    logger.info(f"Total of beams for round 1 : {solve_tachyon_one(manifold, logger)[1]}")
    logger.info(f"Total of beams for round 2 : {solve_tachyon_two(manifold, logger)}")

if __name__ == "__main__":
    main()
