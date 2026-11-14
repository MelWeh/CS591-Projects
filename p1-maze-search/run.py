"""Runs every algorithm on every maze and prints the results for the report."""

from pathlib import Path
from maze import Maze, SingleGoalProblem, MultiGoalProblem, draw
from bfs import bfs
from astar import astar, manhattan, farthest_manhattan, farthest_maze

RESULTS = Path(__file__).parent / "results"
RESULTS.mkdir(exist_ok=True)
LIMIT = 2_000_000  # Part 2 cap on expanded nodes


def report(name, label, maze, problem, path, stats):
    print(f"\n=== {name} | {label} ===")
    if path is None:
        print(f"No solution (stopped after {stats['expanded']} expansions)")
        return
    picture = draw(maze, path, problem)
    print(picture)
    print(f"Path cost:      {len(path) - 1}")
    print(f"Nodes expanded: {stats['expanded']}")
    print(f"Max depth:      {stats['max_depth']}")
    print(f"Max fringe:     {stats['max_fringe']}")
    safe = label.replace("*", "star").replace(" ", "_")
    out = RESULTS / f"{name}_{safe}.txt"
    out.write_text(picture + "\n")


print("========== PART 1 ==========")
for name in ["smallMaze", "mediumMaze", "bigMaze", "openMaze"]:
    maze = Maze(name + ".lay")
    problem = SingleGoalProblem(maze)
    path, stats = bfs(problem)
    report(name, "BFS", maze, problem, path, stats)
    path, stats = astar(problem, manhattan)
    report(name, "A* manhattan", maze, problem, path, stats)

print("\n========== PART 2 ==========")
for name in ["tinySearch", "smallSearch", "trickySearch"]:
    maze = Maze(name + ".lay")
    problem = MultiGoalProblem(maze)
    path, stats = bfs(problem, LIMIT)
    report(name, "BFS", maze, problem, path, stats)
    for h in [farthest_manhattan, farthest_maze]:
        path, stats = astar(problem, h, LIMIT)
        report(name, f"A* {h.__name__}", maze, problem, path, stats)
