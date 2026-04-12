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
    astar,
    print_solution,
)
from src.algorithms.informed import get_heuristic, HEURISTIC_NAMES

import signal
from timeout_utils import TimeoutException, _timeout_handler

import csv
from pathlib import Path

INFORMED_ALGOS = ["greedy", "astar"]

def write_results_to_csv(args, result):
    """
    Append result of a run to performance.csv
    """

    project_root = Path(__file__).resolve().parent
    output_dir = project_root / "analysis" / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "performance.csv"

    write_header = not file_path.exists()

    with open(file_path, mode="a", newline="") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow(
                [
                    "size",
                    "difficulty",
                    "board_name",
                    "algo",
                    "heuristic",
                    "time(s)",
                    "steps",
                    "timeout",
                ]
            )

        # not really necessary considering how performance.sh calls solve, but nice to have
        has_board_cnt = args.board.find(":")
        board_name = (
            f"{args.size}:{args.board}"
            if has_board_cnt != -1
            else f"{args.size}:{args.board}:1"
        )

        if result.get("timeout"):
            time_output = "N/A"
        else:
            time_output = round(result.get("time", 0), 6)

        writer.writerow(
            [
                args.size,
                args.board,
                board_name,
                args.algo.upper(),
                args.heuristic if args.algo in ["greedy", "astar"] else "N/A",
                time_output,
                result.get("steps", 0),
                result.get("timeout", False),
            ]
        )


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


def _run(board: Board, search_fn, timeout: int) -> dict:
    t0 = time.time()

    if timeout > 0:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout)

    try:
        node = search_fn(board.state_key(), board.is_goal, board.get_child_states)
        result = _extract(node)
        result["timeout"] = False
    except TimeoutException:
        result = {"solution": None, "steps": 0, "node": None, "timeout": True}
    finally:
        if timeout > 0:
            signal.alarm(0)

    result["time"] = time.time() - t0
    return result


def _run_informed(board: Board, search_fn, heuristic_name: str, timeout: int) -> dict:
    """Run an informed search algorithm with the specified heuristic."""
    t0 = time.time()
    heuristic_func = get_heuristic(heuristic_name)

    if timeout > 0:
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout)

    try:
        node = search_fn(
            board.state_key(),
            board.is_goal,
            board.get_child_states,
            heuristic_func,
        )
        result = _extract(node)
        result["timeout"] = False
    except TimeoutException:
        result = {"solution": None, "steps": 0, "node": None, "timeout": True}
    finally:
        if timeout > 0:
            signal.alarm(0)

    result["time"] = time.time() - t0
    return result


ALGOS = {
    "bfs": partial(_run, search_fn=breadth_first_search),
    "dfs": partial(_run, search_fn=depth_first_search),
    "ids": partial(_run, search_fn=iterative_deepening_search),
    "greedy": partial(_run_informed, search_fn=greedy_search),
    "astar": partial(_run_informed, search_fn=astar),
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
    parser.add_argument(
        "--heuristic",
        type=str,
        default="",
        choices=HEURISTIC_NAMES,
        help="Heuristic for informed search (default: adjacency)",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=150,
        help="Timeout in seconds. Set to 0 for no limit (default: 150)",
    )

    args = parser.parse_args()

    # Validation: warn if heuristic specified for uninformed algorithm
    uninformed = ["bfs", "dfs", "ids"]
    if args.algo in uninformed and args.heuristic != "":
        print(
            f"Warning: --heuristic is ignored for uninformed algorithm '{args.algo}'\n"
        )

    board = load_board(args.size, args.board)

    print(f"\nSize   : {args.size}")
    print(f"Board  : {args.board}")
    print(f"Slots  : {list(board.slots)}")
    print(f"Algo   : {args.algo.upper()}")
    if args.algo in INFORMED_ALGOS:
        print(f"Heur   : {args.heuristic}")
    print(f"Solved : {board.is_goal(board.state_key())}")
    print()

    if board.is_goal(board.state_key()):
        print("Board is already solved.")
        return

    # Pass heuristic_name to informed algorithms
    if args.algo in INFORMED_ALGOS:
        result = ALGOS[args.algo](
            board, heuristic_name=args.heuristic, timeout=args.timeout
        )
    else:
        result = ALGOS[args.algo](board, timeout=args.timeout)

    sol = result["solution"]

    if result.get("timeout"):
        print(f"\n[!] Search aborted: Timed out after {args.timeout} seconds!")
        time_display = "N/A"
    elif sol is None:
        print("No solution found.")
        time_display = f"{result['time']:.4f}s"
    else:
        print_solution(result["node"])
        time_display = f"{result['time']:.4f}s"

    print(f"Time : {time_display}")

    write_results_to_csv(args, result)


if __name__ == "__main__":
    main()
