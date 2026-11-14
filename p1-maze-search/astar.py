"""A* search and heuristics (works for both Part 1 and Part 2)."""

import heapq
import itertools
from maze import build_path


def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------- Heuristics ----------
def manhattan(state, problem):
    """Part 1: Manhattan distance to the single goal."""
    return manhattan_dist(problem.position(state), problem.goal)


def farthest_manhattan(state, problem):
    """Part 2: Manhattan distance to the farthest dot still left."""
    pos, dots_left = state
    if not dots_left:
        return 0
    return max(manhattan_dist(pos, d) for d in dots_left)


def farthest_maze(state, problem):
    """Part 2: real walking distance to the farthest dot still left."""
    pos, dots_left = state
    if not dots_left:
        return 0
    return max(problem.dist[d][pos] for d in dots_left)


# ---------- A* ----------
def astar(problem, heuristic, max_expansions=None):
    start = problem.start_state()
    counter = itertools.count()
    g = {start: 0}
    parent = {start: None}
    frontier = [(heuristic(start, problem), 0, next(counter), start)]
    closed = set()
    stats = {"expanded": 0, "max_depth": 0, "max_fringe": 1}

    while frontier:
        f, neg_g, _, state = heapq.heappop(frontier)
        if state in closed:
            continue
        closed.add(state)
        stats["expanded"] += 1
        stats["max_depth"] = max(stats["max_depth"], g[state])

        if problem.is_goal(state):
            return build_path(parent, state), stats

        if max_expansions and stats["expanded"] >= max_expansions:
            break

        for nxt in problem.successors(state):
            new_g = g[state] + 1
            if nxt not in g or new_g < g[nxt]:
                g[nxt] = new_g
                parent[nxt] = state
                f_nxt = new_g + heuristic(nxt, problem)
                heapq.heappush(frontier, (f_nxt, -new_g, next(counter), nxt))

        stats["max_fringe"] = max(stats["max_fringe"], len(frontier))

    return None, stats
