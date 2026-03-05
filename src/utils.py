from board import Board

def checkWinner(board : Board) -> bool:
    # deep down justs checks if deque is ordered

    prev: int = board.slots[0]
    for i in range(1, len(board.slots)):
        if prev > board.slots[i]:
            return False
        
    return True
