import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.premade import CONFIGS

def getBoardsData():
    """
    Parse available boards (CONFIGS) to a simple csv
    """

    out_file = os.path.join(os.path.dirname(__file__), "../data/available_boards.csv")

    with open(out_file, "w") as f:
        f.write("size,diff,board_cnt\n")

        for size, entry in CONFIGS.items():
            for diff, boards in entry.items():
                cnt = 1
                for _ in boards:
                    f.write(f"{size},{diff},{cnt}\n")
                    cnt += 1
        
if __name__ == "__main__":
    getBoardsData()
    print("Generated csv with all boards!")
