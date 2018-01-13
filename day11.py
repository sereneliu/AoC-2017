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

with open('day11.txt') as puzzle_file:
    puzzle_input = puzzle_file.read().split(',')

instruction_coordinates = []

def end_hex(x, y, z, instructions):
    hex_coordinates = [x, y, z]
    directions = {
        "n": (0, 1, -1),
        "ne": (1, 0, -1),
        "se": (1, -1, 0),
        "s": (0, -1, 1),
        "sw": (-1, 0, 1),
        "nw": (-1, 1, 0)
    }
    for instruction in instructions:
        x += directions[instruction][0]
        y += directions[instruction][1]
        z += directions[instruction][2]
        hex_coordinates = (x, y, z)
        instruction_coordinates.append(hex_coordinates)
    return hex_coordinates

def shortest_dist(x, y, z, instructions):
    start = (x, y, z)
    end = end_hex(x, y, z, instructions)
    return max(abs(end[0] - start[0]), abs(end[1] - start[1]), abs(end[2] - start[2]))

print shortest_dist(0, 0, 0, puzzle_input) # answer: 670

# --- Part Two ---

# How many steps away is the furthest he ever got from his starting position?

def longest_dist(x, y, z, coordinates):
    max_dist = 0
    for coordinate in coordinates:
        start = (x, y, z)
        end = coordinate
        max_dist = max(max_dist, max(abs(end[0] - start[0]), abs(end[1] - start[1]), abs(end[2] - start[2])))
    return max_dist

print longest_dist(0, 0, 0, instruction_coordinates) # answer: 1426