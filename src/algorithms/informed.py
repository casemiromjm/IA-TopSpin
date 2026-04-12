"""Registry and utilities for informed search algorithms."""

from .heuristics import adjacency_heuristic, min_misplaced_slots

HEURISTICS = {
    "adjacency": adjacency_heuristic,
    "min_misplaced_slots": min_misplaced_slots,
}

HEURISTIC_NAMES = ["adjacency", "min_misplaced_slots"]


def get_heuristic(name: str):
    """Get heuristic function by name.

    Args:
        name: Name of the heuristic function

    Returns:
        Heuristic function that takes a state and returns an int
    """
    if name is None or name.lower() not in HEURISTICS:
        return HEURISTICS["adjacency"]  # Default
    return HEURISTICS[name.lower()]
