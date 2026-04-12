#!/bin/bash

cd "$(dirname "$0")/../../" || exit 1

UNINFORMED_ALGOS=("bfs" "dfs" "ids")
INFORMED_ALGOS=("greedy" "astar")
HEURISTICS=("adjacency" "min_misplaced_slots")

# make sure it has all boards
echo "Generating available boards CSV..."
uv run analysis/scripts/parser.py

IN_CSV_FILE="statistics/data/boards/available_boards.csv"
if [[ ! -f "$IN_CSV_FILE"]]; then
    echo "Error: $IN_CSV_FILE not found! Did the parser fail?"
    exit 1
fi

skip_headers=1
while IFS=, read -r size diff board_cnt; do

    size=$(echo "$size" | tr -d '\r')
    diff=$(echo "$diff" | tr -d '\r')

    if ((skip_headers)); then
        ((skip_headers--))
        continue
    fi

    for algo in "${UNINFORMED_ALGOS[@]}"; do
        echo "  -> Running $algo..."
        for i in 1 2 3; do
            uv run solve.py --size "$size" --board "$diff" --algo "$algo"
        done
    done

    for algo in "${INFORMED_ALGOS[@]}"; do
        for heuristic in "${HEURISTICS[@]}"; do
            echo "  -> Running $algo with $heuristic..."
            for i in 1 2 3; do
                uv run solve.py --size "$size" --board "$diff" --algo "$algo" --heuristic "$heuristic"
            done
        done
    done

done < "$IN_CSV_FILE"
