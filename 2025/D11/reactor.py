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
    result = []
    max_row = 0
    max_col = 0
    with open(path, "r") as f:
        for line in f:
            if not line:
                continue
            rack = tuple(line.strip().split(":"))
            device = rack[0]
            connections = list(rack[1].strip().split(" "))
            result.append((device, connections))
    return result

# We don't need to cache results as it's a directed graph with no cycles on valid paths
@lru_cache(maxsize=None)
def count_paths_two(graph, source_node, target_node, fft_idx, dac_idx, seen_fft, seen_dac):
    if source_node == target_node:
        return int(seen_fft and seen_dac)

    total = 0
    for next_source in graph.iterNeighbors(source_node):
        total += count_paths_two(graph, next_source, target_node, fft_idx, dac_idx, seen_fft or (next_source == fft_idx), seen_dac or (next_source == dac_idx))
    return total

# We don't need to cache results as it's a directed graph with no cycles on valid paths
@lru_cache(maxsize=None)
def count_paths_one(graph, source_node, target_node) -> int:
    if source_node == target_node:
        return 1

    total = 0
    for next_source in graph.iterNeighbors(source_node):
        total += count_paths_one(graph, next_source, target_node)
    return total

def solve_reactor(reactor, source_node, target_node, logger, debug=False, two=False):
    nodes = [rack[0] for rack in reactor]
    edges = [(rack[0], connection, 1) for rack in reactor for connection in rack[1]]

    nodes = sorted({src for src, dst, weight in edges} | {dst for src, dst, weight in edges})
    node_index = {label: index for index, label in enumerate(nodes)}

    devices_graph = nk.Graph(len(nodes), weighted=True, directed=True)

    for src, dst, weight in edges:
        devices_graph.addEdge(node_index[src], node_index[dst], weight)

    src = node_index[source_node]
    tgt = node_index[target_node]
    fft_idx = node_index['fft']
    dac_idx = node_index['dac']

    if two:
        return count_paths_two(devices_graph, src, tgt, fft_idx, dac_idx, False, False)
    else:
        return count_paths_one(devices_graph, src, tgt)

def main():
    parser = argparse.ArgumentParser(description="Read file and split each line into digits.")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Enable debug output"
    )
    parser.add_argument("source_node")
    parser.add_argument("target_node")

    args = parser.parse_args()

    logger = Logger(debug=args.debug)

    reactor = read_file(args.input_file)

    logger.debug(reactor)

    logger.info(f"Total of paths for round 1 : {solve_reactor(reactor, args.source_node, args.target_node, logger, two=False)}")
    logger.info(f"Total of paths for round 2 : {solve_reactor(reactor, args.source_node, args.target_node, logger, two=True)}")

if __name__ == "__main__":
    main()
