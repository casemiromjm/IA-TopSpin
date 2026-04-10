from collections import deque
import heapq  # min-heap

from .node import TreeNode


def print_solution(node):
    """Traces back from the goal node to the root using parent links to print the sequence of states found by the search."""
    path = []

    while node is not None:
        path.append(node.state)
        node = node.parent

    path.reverse()

    print(f"\nSolution found in {len(path) - 1} steps:")
    for i, state in enumerate(path):
        print(f"Step {i}: {state}")


def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    queue = deque([root])
    visited = {initial_state}

    while queue:
        node = queue.popleft()

        if goal_state_func(node.state):
            return node

        for next_state, cost in operators_func(node.state):
            if next_state not in visited:
                visited.add(next_state)
                child = TreeNode(next_state, parent=node)
                node.add_child(child)
                queue.append(child)
    return None


def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    stack = [root]
    visited = {initial_state}

    while stack:
        node = stack.pop()

        if goal_state_func(node.state):
            return node

        children = operators_func(node.state)

        for state, cost in children:
            if state not in visited:
                visited.add(state)
                child = TreeNode(state, parent=node)
                node.add_child(child)
                stack.append(child)

    return None


def depth_limited_search(node, goal_state_func, operators_func, limit):
    stack = [(node, 0)]
    visited_this_path = {node.state}

    while stack:
        current_node, current_depth = stack.pop()

        if goal_state_func(current_node.state):
            return current_node

        if current_depth < limit:
            for next_state, cost in reversed(operators_func(current_node.state)):
                if next_state not in visited_this_path:
                    child = TreeNode(next_state, parent=current_node)
                    stack.append((child, current_depth + 1))
                    visited_this_path.add(next_state)

    return None


def iterative_deepening_search(
    initial_state, goal_state_func, operators_func, max_depth=1000
):
    for depth in range(max_depth + 1):
        root = TreeNode(initial_state)
        result = depth_limited_search(root, goal_state_func, operators_func, depth)
        if result:
            return result
    return None


def greedy_search(initial_state, goal_state_func, operators_func, heuristic_func):
    """Greedy best-first search using only heuristic value.

    Expands nodes with the lowest heuristic value first.
    Not guaranteed to find the optimal solution.

    Args:
        initial_state: Starting state
        goal_state_func: Function to check if state is goal
        operators_func: Function to get child states
        heuristic_func: Heuristic function for states

    Returns:
        TreeNode: Goal node if found, None otherwise
    """
    root = TreeNode(initial_state)
    queue = [(heuristic_func(root.state), root)]
    visited = {initial_state}

    while queue:
        _, node = queue.pop(0)

        if goal_state_func(node.state):
            return node

        for next_state, cost in operators_func(node.state):
            if next_state not in visited:
                visited.add(next_state)
                child = TreeNode(next_state, parent=node)
                node.add_child(child, cost)
                queue.append((heuristic_func(child.state), child))

        # Sort queue by heuristic value
        queue.sort(key=lambda x: x[0])

    return None


def astar(initial_state, goal_state_func, operators_func, heuristic_func):
    """
    A* Algorithm

    Args:
        initial_state: Starting state
        goal_state_func: Function to check if state is goal
        operators_func: Function to get child states
        heuristic_func: Heuristic function for states

    Returns:
        TreeNode: Goal node if found, None otherwise
    """

    root = TreeNode(initial_state)
    queue = []
    # initial g is 0
    heapq.heappush(queue, (heuristic_func(root.state), root))
    visited = set()

    while queue:
        node: TreeNode
        _, node = heapq.heappop(queue)
        visited.add(node.state)

        if goal_state_func(node.state):
            return node

        for next_state, cost in operators_func(node.state):
            if next_state not in visited:
                child = TreeNode(next_state, parent=node)
                # g = current cost (node.cost) + cost of the next move (cost)
                node.add_child(child, operator_cost=cost)
                # calculates h, f = g + h
                f_score = child.cost + heuristic_func(next_state)
                heapq.heappush(queue, (f_score, child))

    return None
