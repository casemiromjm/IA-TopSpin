"""Terminal solver for Top Spin.

Usage:
    python3 solve.py --size 6 --board easy --algo bfs
    python3 solve.py --size 6 --board easy:2 --algo dfs
    python3 solve.py --size 10 --board medium:1 --algo ids
    python3 solve.py --size 14 --board hard --algo ids
    python3 solve.py --size 20 --board easy --algo bfs
    python3 solve.py --size 20 --board random --algo dfs

--board format:  random | <difficulty> | <difficulty>:<number>
  e.g.  easy        ->  easy board #1
        easy:2      ->  easy board #2
        medium      ->  medium board #1
        random      ->  random shuffle
"""

import argparse
import time
from functools import partial

from src.board import Board
from src.premade import get as get_config, CONFIGS
from src.algorithms.search import (
    breadth_first_search,
    depth_first_search,
    iterative_deepening_search,
    greedy_search,
    print_solution,
)
from src.algorithms.heuristics import adjacency_heuristic


def _states_to_moves(path: list) -> list[str]:
    moves = []
    for i in range(len(path) - 1):
        s, ns = path[i], path[i + 1]
        if s[1:] + (s[0],) == ns:
            moves.append("left")
        elif (s[-1],) + s[:-1] == ns:
            moves.append("right")
        else:
            moves.append("rotate")
    return moves


def _extract(node) -> dict:
    if node is None:
        return {"solution": None, "steps": 0, "node": None}
    path = []
    cur = node
    while cur:
        path.append(cur.state)
        cur = cur.parent
    path.reverse()
    return {"solution": _states_to_moves(path), "steps": len(path) - 1, "node": node}


def _run(board: Board, search_fn) -> dict:
    t0 = time.time()
    node = search_fn(board.state_key(), board.is_goal, board.get_child_states)
    result = _extract(node)
    result["time"] = time.time() - t0
    return result


def _run_greedy(board: Board) -> dict:
    t0 = time.time()
    node = greedy_search(
        board.state_key(),
        board.is_goal,
        board.get_child_states,
        adjacency_heuristic,
    )
    result = _extract(node)
    result["time"] = time.time() - t0
    return result


ALGOS = {
    "bfs": partial(_run, search_fn=breadth_first_search),
    "dfs": partial(_run, search_fn=depth_first_search),
    "ids": partial(_run, search_fn=iterative_deepening_search),
    "greedy": _run_greedy,
}


def load_board(size: int, board_arg: str) -> Board:
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
            f"Available: 1-{available}."
        )
    return Board(config=list(slots))


def main():
    parser = argparse.ArgumentParser(description="Top Spin solver")
    parser.add_argument("--size", type=int, default=6, choices=[6, 10, 14, 20])
    parser.add_argument(
        "--board",
        type=str,
        default="random",
        help="random | <difficulty> | <difficulty>:<number>",
    )
    parser.add_argument("--algo", type=str, default="bfs", choices=list(ALGOS.keys()))

    args = parser.parse_args()

    board = load_board(args.size, args.board)

    print(f"\nSize   : {args.size}")
    print(f"Board  : {args.board}")
    print(f"Slots  : {list(board.slots)}")
    print(f"Algo   : {args.algo.upper()}")
    print(f"Solved : {board.is_goal(board.state_key())}")
    print()

    if board.is_goal(board.state_key()):
        print("Board is already solved.")
        return

    result = ALGOS[args.algo](board)
    sol = result["solution"]

    if sol is None:
        print("No solution found.")
    else:
        print_solution(result["node"])

    print(f"Time : {result['time']:.4f}s")


if __name__ == "__main__":
    main()
