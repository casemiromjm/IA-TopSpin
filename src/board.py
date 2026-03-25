from __future__ import annotations

from collections import deque
from copy import deepcopy
from random import shuffle


class Board:
    """Top Spin board: a circular track of numbered slots with a rotate window."""

    slots: deque[int]
    moves: int
    rotate_size: int  # how many front slots the mechanism flips

    def __init__(
        self, size: int = 20, rotate_size: int = 4, config: list[int] | None = None
    ):
        """Create a board.

        *size*: number of slots (ignored when *config* is provided).
        *rotate_size*: how many leading slots the rotate action flips.
        *config*: explicit starting permutation; if None a random shuffle is used.
        """
        if config is not None:
            self.slots = deque(config)
        else:
            self.slots = deque(range(1, size + 1))
            shuffle(self.slots)

        self.rotate_size = rotate_size
        self.moves = 0

    # ── actions ───────────────────────────────────────────────────────────

    def rotate(self) -> None:
        """Reverse the first *rotate_size* slots in place."""
        window = list(self.slots)[: self.rotate_size]
        window.reverse()
        for i, v in enumerate(window):
            self.slots[i] = v
        self.moves += 1

    def move_right(self) -> None:
        """Shift the whole track one position clockwise."""
        self.slots.rotate(1)
        self.moves += 1

    def move_left(self) -> None:
        """Shift the whole track one position counter-clockwise."""
        self.slots.rotate(-1)
        self.moves += 1

    # ── queries ───────────────────────────────────────────────────────────

    def copy(self) -> Board:
        return deepcopy(self)

    def state_key(self) -> tuple[int, ...]:
        """Hashable snapshot for visited-set membership."""
        return tuple(self.slots)

    def __repr__(self) -> str:
        return f"Board({list(self.slots)}, moves={self.moves})"

    # ── functional interface for search algorithms ─────────────────────────

    def is_goal(self, state: tuple[int, ...]) -> bool:
        """Check if a tuple state is the goal (1..n in order from any start)."""
        n = len(state)
        try:
            start = state.index(1)
        except ValueError:
            return False
        return all(state[(start + i) % n] == i + 1 for i in range(n))

    def get_child_states(
        self, state: tuple[int, ...]
    ) -> list[tuple[tuple[int, ...], int]]:
        """Return successor states for search algorithms."""
        left = state[1:] + (state[0],)
        right = (state[-1],) + state[:-1]
        lst = list(state)
        lst[: self.rotate_size] = lst[: self.rotate_size][::-1]
        rotated = tuple(lst)
        return [(left, 1), (right, 1), (rotated, 1)]
