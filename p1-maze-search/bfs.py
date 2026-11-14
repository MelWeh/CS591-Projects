"""Breadth-first search (works for both Part 1 and Part 2)."""

from collections import deque
from maze import build_path


def bfs(problem, max_expansions=None):
    start = problem.start_state()
    frontier = deque([start])
    parent = {start: None}
    depth = {start: 0}
    stats = {"expanded": 0, "max_depth": 0, "max_fringe": 1}

    while frontier:
        state = frontier.popleft()
        stats["expanded"] += 1
        stats["max_depth"] = max(stats["max_depth"], depth[state])

        if problem.is_goal(state):
            return build_path(parent, state), stats

        if max_expansions and stats["expanded"] >= max_expansions:
            break

        for nxt in problem.successors(state):
            if nxt not in parent:
                parent[nxt] = state
                depth[nxt] = depth[state] + 1
                frontier.append(nxt)

        stats["max_fringe"] = max(stats["max_fringe"], len(frontier))

    return None, stats
