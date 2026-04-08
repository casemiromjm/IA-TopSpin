"""
Terminal usage:
    python3 -m src.premade                          # list all
    python3 -m src.premade --size 6 --diff easy     # list specific
"""

# CONFIGS[size][difficulty] = list of boards (each a tuple of slots)
CONFIGS: dict[int, dict[str, list[tuple]]] = {
    6: {
        "easy": [
            (4, 3, 2, 1, 5, 6),
            (1, 2, 6, 5, 4, 3),
            (1, 2, 3, 5, 6, 4),
        ],
        "medium": [
            (3, 1, 2, 4, 5, 6),
            (2, 3, 1, 4, 5, 6),
            (1, 2, 3, 6, 5, 4),
        ],
        "hard": [
            (6, 5, 4, 3, 2, 1),
            (1, 2, 5, 6, 4, 3),
            (2, 1, 4, 3, 6, 5),
        ],
    },
    10: {
        "easy": [
            (4, 3, 2, 1, 5, 6, 7, 8, 9, 10),
            (3, 4, 5, 1, 2, 6, 7, 8, 9, 10),
            (1, 2, 3, 4, 5, 6, 10, 9, 8, 7),
        ],
        "medium": [
            (2, 3, 4, 5, 6, 1, 7, 8, 9, 10),
            (1, 2, 3, 4, 9, 10, 5, 6, 7, 8),
            (1, 4, 5, 6, 7, 8, 9, 10, 2, 3),
        ],
        "hard": [
            (10, 9, 8, 7, 6, 5, 4, 3, 2, 1),
            (1, 8, 5, 2, 9, 6, 3, 10, 7, 4),
            (1, 4, 7, 10, 3, 6, 9, 2, 5, 8),
        ],
    },
    14: {
        "easy": [
            (4, 3, 2, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14),
            (1, 2, 3, 13, 14, 4, 5, 6, 7, 8, 9, 10, 11, 12),
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 13, 12, 11),
        ],
        "medium": [
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 10, 11, 12),
            (1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 4, 5, 6, 7),
            (1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 5, 6, 7),
        ],
        "hard": [
            (14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1),
            (7, 3, 11, 1, 9, 5, 13, 2, 8, 4, 12, 6, 14, 10),
            (14, 1, 13, 2, 12, 3, 11, 4, 10, 5, 9, 6, 8, 7),
        ],
    },
    20: {
        "easy": [
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 19),
            (2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
            (4, 3, 2, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
        ],
        "medium": [
            (4, 3, 2, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 19, 18, 17),
            (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 1, 2, 3, 5, 4),
            (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 1, 2, 3, 4, 5, 6, 8, 7, 9, 10),
        ],
        "hard": [
            (20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1),
            (10, 1, 12, 3, 14, 5, 16, 7, 18, 9, 20, 2, 11, 4, 13, 6, 15, 8, 17, 19),
            (20, 1, 19, 2, 18, 3, 17, 4, 16, 5, 15, 6, 14, 7, 13, 8, 12, 9, 11, 10),
        ],
    },
}

# returns slots for a given size and difficulty of a board, or None if not found


def get(size: int, difficulty: str, board_num: int) -> tuple | None:
    boards = CONFIGS.get(size, {}).get(difficulty.lower(), [])
    if 1 <= board_num <= len(boards):
        return boards[board_num - 1]
    return None


# count available boards for a given size and difficulty


def count(size: int, difficulty: str) -> int:
    return len(CONFIGS.get(size, {}).get(difficulty.lower(), []))


# main function for testing

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, choices=[6, 10, 14, 20])
    parser.add_argument("--diff", choices=["easy", "medium", "hard"])
    args = parser.parse_args()

    sizes = [args.size] if args.size else [6, 10, 14, 20]
    diffs = [args.diff] if args.diff else ["easy", "medium", "hard"]

    for size in sizes:
        print(f"\nSize {size}:")
        for diff in diffs:
            boards = CONFIGS.get(size, {}).get(diff, [])
            print(f"  {diff.capitalize()} ({len(boards)} boards):")
            for i, slots in enumerate(boards, 1):
                print(f"    #{i}: {list(slots)}")
