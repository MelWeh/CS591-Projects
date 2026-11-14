"""Shared code: loading mazes, problem definitions, drawing paths."""

from collections import deque
from pathlib import Path

MAZE_DIR = Path(__file__).parent / "mazes"
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right


# ---------- Loading ----------
class Maze:
    def __init__(self, filename):
        self.lines = (MAZE_DIR / filename).read_text().splitlines() # opens .lay file and reads it into a list of strings
        self.walls = set()
        self.dots = set()
        self.start = None
        for r, line in enumerate(self.lines):   # loops over every character, with r as the row number
            for c, ch in enumerate(line):       # and c as the column number
                if ch == "%":
                    self.walls.add((r, c))      # adds the coordinates of the wall to the walls set
                elif ch == "P":
                    self.start = (r, c)         # sets the start position to the coordinates of the player
                elif ch == ".":
                    self.dots.add((r, c))       # adds the coordinates of the dot to the dots set

    def neighbors(self, pos):
        r, c = pos
        for dr, dc in MOVES:
            nxt = (r + dr, c + dc)
            if nxt not in self.walls:
                yield nxt


def maze_distances(maze, source):
    """Real walking distance from source to every reachable cell (plain BFS)."""
    dist = {source: 0}
    queue = deque([source])
    while queue:
        pos = queue.popleft()
        for nxt in maze.neighbors(pos):
            if nxt not in dist:
                dist[nxt] = dist[pos] + 1
                queue.append(nxt)
    return dist


# ---------- Problems ----------
class SingleGoalProblem:
    """Part 1: state = (row, col)."""

    def __init__(self, maze):
        self.maze = maze
        self.goal = next(iter(maze.dots))

    def start_state(self):
        return self.maze.start

    def is_goal(self, state):
        return state == self.goal

    def successors(self, state):
        return list(self.maze.neighbors(state))

    def position(self, state):
        return state


class MultiGoalProblem:
    """Part 2: state = ((row, col), frozenset of dots not yet eaten)."""

    def __init__(self, maze):
        self.maze = maze
        # Precompute walking distances from every dot (used by a heuristic).
        self.dist = {dot: maze_distances(maze, dot) for dot in maze.dots}

    def start_state(self):
        pos = self.maze.start
        return (pos, frozenset(self.maze.dots - {pos}))

    def is_goal(self, state):
        return len(state[1]) == 0

    def successors(self, state):
        pos, dots_left = state
        result = []
        for nxt in self.maze.neighbors(pos):
            result.append((nxt, dots_left - {nxt}))
        return result

    def position(self, state):
        return state[0]


# ---------- Helpers ----------
def build_path(parent, state):
    """Follow parent links back from the goal to the start."""
    path = []
    while state is not None:
        path.append(state)
        state = parent[state]
    path.reverse()
    return path


def draw(maze, path, problem):
    """Return the maze as text with '.' on every square of the path."""
    grid = [list(line) for line in maze.lines]
    for state in path:
        r, c = problem.position(state)
        grid[r][c] = "."
    return "\n".join("".join(row) for row in grid)
