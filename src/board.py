from typing import Tuple


class Board:
    def __init__(
        self, size: int = 20, spin_size: int = 4, initial_state: Tuple[int, ...] = None
    ):
        self.size = size
        self.spin_size = spin_size
        if initial_state is not None:
            self.state = initial_state
        else:
            self.state = tuple(range(1, size + 1))

    def move_left(state: Tuple[int, ...]):
        return state[1:] + (state[0],), 1

    def move_right(state: Tuple[int, ...]):
        return (state[-1],) + state[:-1], 1

    def spin(state: Tuple[int, ...]):
        lst = list(state)
        segment = lst[: state.spin_size]
        lst[: state.spin_size] = segment[::-1]
        return tuple(lst), 1

    def is_goal(self, state: Tuple[int, ...]) -> bool:
        return state == tuple(range(1, self.size + 1))
