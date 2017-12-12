# --- Day 11: Hex Ed ---

# Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

# Fortunately for her, you have plenty of experience with infinite grids.

# Unfortunately for you, it's a hex grid.

# The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast, southeast, south, southwest, and northwest:

#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \

# You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

# For example:

# ne,ne,ne is 3 steps away.
# ne,ne,sw,sw is 0 steps away (back where you started).
# ne,ne,s,s is 2 steps away (se,se).
# se,sw,se,sw,sw is 3 steps away (s,s,sw).

from __future__ import print_function
import functools

with open("day11.txt", "r") as puzzle_file:
    puzzle_input = puzzle_file.read().split(",")

directions = {
    "n": (0, 1, -1),
    "ne": (1, 0, -1),
    "se": (1, -1, 0),
    "s": (0, -1, 1),
    "sw": (-1, 0, 1),
    "nw": (-1, 1, 0)
}

def move_hex(point, instruction):
    x, y, z = point
    dx, dy, dz = directions[instruction]
    return (x + dx, y + dy, z + dz)

def distance_to_origin(point):
    x, y, z = point
    return max(abs(x), abs(y), abs(z))

# --- Part Two ---

# How many steps away is the furthest he ever got from his starting position?

def move_and_max(current, instruction):
    last_point, max_distance = current
    next_point = move_hex(last_point, instruction)
    return (next_point, max(max_distance, distance_to_origin(next_point)))

last_point, max_distance = functools.reduce(
        move_and_max, puzzle_input, ((0, 0, 0), 0))

print(distance_to_origin(last_point))
print(max_distance)
