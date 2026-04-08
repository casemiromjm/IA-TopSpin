"""Heuristic functions for informed search algorithms."""


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
