from random import shuffle
from collections import deque

import utils

class Board:
    slots: deque[int]
    moves: int

    def __init__(self):
        # initialize the board with the shuffled slots
        self.slots = deque([x for x in range (1, 21)])
        shuffle(self.slots)

        self.moves = 0

    def rotate(self):
        ''' rotate 4 slots. consider that the 4 slots able to rotate are always at the beginning of the array (deque) for simplicity '''
        self.slots[0], self.slots[3] = self.slots[3], self.slots[0]
        self.slots[1], self.slots[2] = self.slots[2], self.slots[1]

    def move_right(self):
        self.slots.rotate(1)

        self.moves += 1

    def move_left(self):
        self.slots.rotate(-1)
        
        self.moves += 1


def main() -> None:
    '''function for simple testing'''
    b: Board = Board()
    print(b.slots)
    b.rotate()
    print(b.slots)

    print(utils.checkWinner(b))

if __name__ == "__main__":
    main()
