#!/usr/bin/env python3

import argparse
import ast
import itertools
import multiprocessing as mp
import numpy as np
import sys

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from scipy.optimize import Bounds, LinearConstraint, milp

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
            machine = list(line.strip().split(" "))
            if not line:
                continue
            result.append((machine[0], machine[1:-1], machine[-1]))
    return result

def convert_lights(lights):
    lights = lights.translate(str.maketrans("", "", "[]"))
    bool_lights = []

    for index, light in enumerate(lights):
        if light == ".":
            bool_lights.append(False)
        if light == "#":
            bool_lights.append(True)

    return bool_lights

def convert_joltages(joltages):
    joltages = joltages.translate(str.maketrans("", "", "{}"))
    return [int(joltage) for joltage in joltages.split(",")]

def convert_buttons(button_sequence):
    buttons = []
    for button in button_sequence:
        buttons.append([int(b.translate(str.maketrans("","","()"))) for b in button.split(",")])

    return buttons

def do_monkey_press(sequence, expected, logger):
    state = [False for i in range(0, len(expected))]
    press_count = 0

    for index, button_press in enumerate(sequence):
        press_count += 1
        for press in button_press:
            state[press] = not(state[press])

    if state == expected and press_count == len(sequence):
        logger.debug(f"Found: {sequence} leads to {expected} in {press_count} button presses")
        return press_count, expected

    # Monkey found nothing: DASDLKASLDKASLDKSADDJAKSICHICNHIEWQCNWEICFNWEC !
    return 9999, expected

def solve_factory_one(machine, logger):
    result_lights = convert_lights(machine[0])
    button_seq = convert_buttons(machine[1])
    dont_care = convert_joltages(machine[2])

    all_seqs = []
    button_presses = []

    # Generate all possible button sequences for that machine
    for idx in range(1, len(button_seq) + 1):
        all_seqs.extend(itertools.combinations(button_seq, idx))

    # Go monkeys !
    compute_fn = partial(do_monkey_press, logger=logger, expected=result_lights)
    with ThreadPoolExecutor() as executor:
        button_presses = list(executor.map(compute_fn, all_seqs))

    return min(button_presses)

def solve_factory_two(factory, logger):
    total_button_presses = 0

    for machine in factory:
        result_lights = convert_lights(machine[0])
        button_seq = convert_buttons(machine[1])
        joltages = convert_joltages(machine[2])

        num_lights = len(result_lights)
        num_buttons = len(button_seq)

        logger.debug(f"{result_lights} {button_seq} {joltages}")

        cost_vector = np.ones(num_buttons)
        targets = np.array(joltages)
        coeffs = np.zeros((num_lights, num_buttons))

        for index, button in enumerate(button_seq):
            for number in button:
                coeffs[number, index] = 1

        logger.debug(f"Coeefs: {coeffs}\nJoltages: {joltages}")

        # Prepare MILP solver
        contraints = LinearConstraint(coeffs, targets, targets)
        integrality = np.ones(num_buttons)
        bounds = Bounds(lb=0, ub=np.inf)
        result = milp(c=cost_vector, constraints=contraints, integrality=integrality, bounds=bounds)

        if not result.success:
            raise Exception("MILP Failed :(")

        # There's a solution, verify it. Cast to int to avoid rounding issues
        candidate = np.round(result.x).astype(int)
        logger.debug(f"Candidate solution: {result.x} (raw), {candidate} (converted)")

        if not np.all(coeffs @ candidate == targets):
            raise Exception("No solution è.é")

        logger.debug(f"Min press for this machine: {int(np.sum(candidate))}")
        total_button_presses += int(np.sum(candidate))

    return total_button_presses

def solve_factory(fn, factory, logger):
    compute_fn = partial(fn, logger=logger)
    with mp.Pool() as pool:
        min_button_presses = pool.map(compute_fn, factory)

    return sum(presses for presses, _ in min_button_presses)

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

    factory = read_file(args.input_file)

    logger.debug(factory)

    logger.info(f"Total button presses for round 1 : {solve_factory(solve_factory_one, factory, logger)}")
    logger.info(f"Total button presses for round 2 : {solve_factory_two(factory, logger)}")

if __name__ == "__main__":
    main()
