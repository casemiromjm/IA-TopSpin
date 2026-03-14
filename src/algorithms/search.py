from collections import deque

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
