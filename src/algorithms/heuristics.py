"""Heuristic functions for informed search algorithms."""

import math


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

    return breaks


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
