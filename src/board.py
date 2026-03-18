from typing import List, Tuple


class Board:
    def __init__(
        self,
        size: int = 20,
        spin_size: int = 4,
        initial_state: Tuple[int, ...] | None = None,
    ) -> None:
        self.size = size
        self.spin_size = spin_size
        if initial_state is not None:
            self._initial_state = initial_state
        else:
            self._initial_state = tuple(range(1, size + 1))
        self._goal_state = tuple(range(1, size + 1))

    @property
    def initial_state(self) -> Tuple[int, ...]:
        """Return the starting state for this board."""
        return self._initial_state

    @staticmethod
    def move_left(state: Tuple[int, ...]) -> Tuple[Tuple[int, ...], int]:
        """Rotate the ring one position to the left.

        Example: (1, 2, 3) -> ((2, 3, 1), 1)
        """
        return state[1:] + (state[0],), 1

    @staticmethod
    def move_right(state: Tuple[int, ...]) -> Tuple[Tuple[int, ...], int]:
        """Rotate the ring one position to the right.

        Example: (1, 2, 3) -> ((3, 1, 2), 1)
        """
        return (state[-1],) + state[:-1], 1

    def spin(self, state: Tuple[int, ...]) -> Tuple[Tuple[int, ...], int]:
        """Reverse the first `spin_size` elements (the spin window)."""
        lst = list(state)
        segment = lst[: self.spin_size]
        lst[: self.spin_size] = segment[::-1]
        return tuple(lst), 1

    def get_child_states(
        self, state: Tuple[int, ...]
    ) -> List[Tuple[Tuple[int, ...], int]]:
        """Return all successor states from applying each legal move once."""
        return [
            Board.move_left(state),
            Board.move_right(state),
            self.spin(state),
        ]

    def is_goal(self, state: Tuple[int, ...]) -> bool:
        """Check if the state is sorted from 1 to `size` for this board."""
        return state == self._goal_state
