"""Terminal solver for Top Spin.

Usage:
    python3 solve.py --size 6 --board easy --algo bfs
    python3 solve.py --size 6 --board easy:2 --algo dfs
    python3 solve.py --size 10 --board medium:1 --algo bfs
    python3 solve.py --size 6 --board random --algo bfs

--board format:  random | <difficulty> | <difficulty>:<number>
  e.g.  easy        →  easy board #1
        easy:2      →  easy board #2
        medium      →  medium board #1
        random      →  random shuffle
"""

import argparse
import time
from collections import deque

from src.board import Board
from src.premade import get as get_config, CONFIGS


# ─────────────────────────────────────────────────────────────────────────────
# Inline algorithms — temporary until src/algorithms/search.py is filled in.
# ─────────────────────────────────────────────────────────────────────────────

def _run_bfs(board: Board) -> dict:

    return {"solution": [], "states": 0, "time": 0.0}

def _run_dfs(board: Board, max_depth: int = 30) -> dict:
    return {"solution": [], "states": 0, "time": 0.0}

# ─────────────────────────────────────────────────────────────────────────────
# Board loading
# ─────────────────────────────────────────────────────────────────────────────

def load_board(size: int, board_arg: str) -> Board:
    """Parse --board argument and return a Board."""
    if board_arg.lower() == "random":
        return Board(size=size)

    if ":" in board_arg:
        diff, num_str = board_arg.split(":", 1)
        num = int(num_str)
    else:
        diff = board_arg
        num = 1

    slots = get_config(size, diff, num)
    if slots is None:
        available = len(CONFIGS.get(size, {}).get(diff.lower(), []))
        if available == 0:
            raise SystemExit(f"No '{diff}' boards for size {size}.")
        raise SystemExit(
            f"Board #{num} not found for size {size} / {diff}. "
            f"Available: 1–{available}."
        )
    return Board(config=list(slots))

ALGOS = {
    "bfs": _run_bfs,
    "dfs": _run_dfs,
}


def main():
    parser = argparse.ArgumentParser(description="Top Spin solver")
    parser.add_argument("--size",  type=int, default=6, choices=[6, 10, 14, 20])
    parser.add_argument("--board", type=str, default="random", help="random | <difficulty> | <difficulty>:<number>")
    parser.add_argument("--algo",  type=str, default="bfs", choices=list(ALGOS.keys()))

    args = parser.parse_args()

    board = load_board(args.size, args.board)

    print(f"\nSize   : {args.size}")
    print(f"Board  : {args.board}")
    print(f"Slots  : {list(board.slots)}")
    print(f"Algo   : {args.algo.upper()}")
    print(f"Solved : {board.is_solved()}")
    print()

    if board.is_solved():
        print("Board is already solved.")
        return

    result = ALGOS[args.algo](board)
    sol = result["solution"]

    if sol is None:
        print("No solution found.")
    else:
        print(f"Solution ({len(sol)} moves): {' -> '.join(sol)}")

    print(f"States visited : {result['states']}")
    print(f"Time           : {result['time']:.4f}s")


if __name__ == "__main__":
    main()
