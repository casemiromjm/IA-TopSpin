"""Pattern database heuristic for the TopSpin puzzle.

Maps abstract states (non-pattern tiles replaced with 0) to minimum
moves needed to reach any goal state. Since abstract cost <= real cost,
this is an admissible heuristic.
"""

from collections import deque


def _abstract(state: tuple[int, ...], pattern: frozenset) -> tuple[int, ...]:
    """Replace non-pattern tiles with 0 wildcard."""
    return tuple(v if v in pattern else 0 for v in state)


def build_pattern_db(n: int, rotate_size: int, pattern: frozenset) -> dict:
    """Build PDB via BFS from all cyclic goal states.

    Every rotation of (1..n) is a valid solved state for TopSpin.
    """
    goal = tuple(range(1, n + 1))
    db: dict = {}
    queue: deque = deque()

    for i in range(n):
        rotated = goal[i:] + goal[:i]
        abstract = _abstract(rotated, pattern)
        if abstract not in db:
            db[abstract] = 0
            queue.append((abstract, 0))

    while queue:
        state, cost = queue.popleft()
        next_cost = cost + 1

        nb = state[1:] + (state[0],)
        if nb not in db:
            db[nb] = next_cost
            queue.append((nb, next_cost))

        nb = (state[-1],) + state[:-1]
        if nb not in db:
            db[nb] = next_cost
            queue.append((nb, next_cost))

        nb = state[:rotate_size][::-1] + state[rotate_size:]
        if nb not in db:
            db[nb] = next_cost
            queue.append((nb, next_cost))

    return db


_cache: dict = {}


def pattern_db_heuristic(state: tuple[int, ...], rotate_size: int = 4) -> int:
    """Lookup heuristic from cached PDB for tiles {1,2,3,4}.

    Returns lower bound on moves to reach goal. Database is built
    lazily and cached for O(1) subsequent lookups.
    """
    n = len(state)
    pattern = frozenset({1, 2, 3, 4})
    cache_key = (n, rotate_size)
    if cache_key not in _cache:
        _cache[cache_key] = build_pattern_db(n, rotate_size, pattern)
    return _cache[cache_key].get(_abstract(state, pattern), 0)


def make_pattern_db_heuristic(rotate_size: int):
    """Create heuristic bound to specific rotate_size."""
    return lambda state: pattern_db_heuristic(state, rotate_size)
