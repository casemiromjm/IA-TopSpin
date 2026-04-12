"""Heuristic functions for informed search algorithms."""

import math
from collections import deque


def adjacency_heuristic(state: tuple[int, ...]) -> int:
    """Count the number of adjacency breaks in the state.

    A break occurs when piece i is not followed by piece i+1.
    Piece N must be followed by piece 1 (circular).

    This is admissible: each rotate operation can fix at most 2 breaks
    (at the edges of the rotation window).

    Args:
        state: Tuple representing the current board state

    Returns:
        Number of breaks in the sequence
    """
    n = len(state)
    breaks = 0

    for i in range(n):
        current = state[i]
        next_pos = (i + 1) % n
        expected_next = (current % n) + 1  # 1 follows N, 2 follows 1, etc.
        if state[next_pos] != expected_next:
            breaks += 1

    return math.ceil(breaks / 2)


def min_misplaced_slots(state: tuple[int, ...]) -> int:
    """
    Calculates the cyclic misplaced slots heuristic by checking all possible rotations of the goal state. Using frequency_map for better performance
    """

    n = len(state)

    shift_counts = [0] * n

    for i, piece in enumerate(state):
        shift = (i - (piece - 1)) % n
        shift_counts[shift] += 1

    # if 20 pieces need a shift 1, it is a winning board shifted by 1
    max_in_place = max(shift_counts)

    min_misplaced = n - max_in_place

    return math.ceil(min_misplaced / 4)


def _abstract(state: tuple[int, ...], pattern: frozenset) -> tuple[int, ...]:
    return tuple(v if v in pattern else 0 for v in state)


def _build_pattern_db(n: int, rotate_size: int, pattern: frozenset) -> dict:
    goal = tuple(range(1, n + 1))
    db: dict = {}
    queue: deque = deque()

    for i in range(n):
        rotated = goal[i:] + goal[:i]
        abstract = _abstract(rotated, pattern)
        if abstract not in db:
            db[abstract] = 0
            queue.append((abstract, 0))

    while queue:
        state, cost = queue.popleft()
        next_cost = cost + 1

        nb = state[1:] + (state[0],)
        if nb not in db:
            db[nb] = next_cost
            queue.append((nb, next_cost))

        nb = (state[-1],) + state[:-1]
        if nb not in db:
            db[nb] = next_cost
            queue.append((nb, next_cost))

        nb = state[:rotate_size][::-1] + state[rotate_size:]
        if nb not in db:
            db[nb] = next_cost
            queue.append((nb, next_cost))

    return db


_PATTERN_DB_CACHE: dict = {}


def pattern_db_heuristic(state: tuple[int, ...], rotate_size: int = 4) -> int:
    n = len(state)
    pattern = frozenset({1, 2, 3, 4})
    cache_key = (n, rotate_size)
    if cache_key not in _PATTERN_DB_CACHE:
        _PATTERN_DB_CACHE[cache_key] = _build_pattern_db(n, rotate_size, pattern)
    return _PATTERN_DB_CACHE[cache_key].get(_abstract(state, pattern), 0)


def make_pattern_db_heuristic(rotate_size: int):
    return lambda state: pattern_db_heuristic(state, rotate_size)
