from typing import Tuple


class Board:
    SPIN_SIZE: int = 4

    def __init__(
        self, size: int = 20, spin_size: int = 4, initial_state: Tuple[int, ...] = None
    ):
        self.size = size
        self.spin_size = spin_size
        if initial_state is not None:
            self.state = initial_state
        else:
            self.state = tuple(range(1, size + 1))

        Board.SPIN_SIZE = spin_size

    @staticmethod
    def move_left(state: Tuple[int, ...]) -> Tuple[Tuple[int, ...], int]:
        """Rotate the ring one position to the left."""
        # (1, 2, 3) -> ((2, 3, 1), 1)
        return state[1:] + (state[0],), 1

    @staticmethod
    def move_right(state: Tuple[int, ...]) -> Tuple[Tuple[int, ...], int]:
        """Rotate the ring one position to the right."""
        # (1, 2, 3) -> ((3, 1, 2), 1)
        return (state[-1],) + state[:-1], 1

    @staticmethod
    def spin(state: Tuple[int, ...]) -> Tuple[Tuple[int, ...], int]:
        """Reverse the first 'spin_size' elements."""
        lst = list(state)
        segment = lst[: Board.SPIN_SIZE]
        lst[: Board.SPIN_SIZE] = segment[::-1]
        return tuple(lst), 1

    @staticmethod
    def get_child_states(state: Tuple[int, ...]):
        """Aggregates all possible moves from the current state."""
        return [
            Board.move_left(state),
            Board.move_right(state),
            Board.spin(state),
        ]

    @staticmethod
    def is_goal(state: Tuple[int, ...]) -> bool:
        """Checks if the state is sorted from 1 to N."""
        return state == tuple(range(1, len(state) + 1))
