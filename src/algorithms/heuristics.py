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


def minimum_misplaced_pieces(state: tuple[int, ...]) -> int:
    """
    Calculates the cyclic misplaced pieces heuristic by checking all possible rotations of the goal state.
    """

    n = len(state)
    min_misplaced = n

    for shift in range(n):
        current_misplaced = 0

        for i in range(n):
            expected_piece = ((i + shift) % n) + 1

            if state[i] != expected_piece:
                current_misplaced = +1

        if current_misplaced < min_misplaced:
            min_misplaced = current_misplaced

    return math.ceil(min_misplaced / 4)
