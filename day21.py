# --- Day 21: Fractal Art ---

# You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail of an image through a set of rules.

# The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always begins with this pattern:

# .#.
# ..#
# ###
# Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

# Then, the program repeats the following process:

# If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3 square by following the corresponding enhancement rule.
# Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square into a 4x4 square by following the corresponding enhancement rule.
# Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

# The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The artist explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the output pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated by slashes. For example, the following rules correspond to the adjacent patterns:

# ../.#  =  ..
#           .#

#                 .#.
# .#./..#/###  =  ..#
#                 ###

#                         #..#
# #..#/..../#..#/.##.  =  ....
#                         #..#
#                         .##.

# When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns match the same rule:

# .#.   .#.   #..   ###
# ..#   #..   #.#   ..#
# ###   ###   ##.   .#.

# Suppose the book contained the following two rules:

# ../.# => ##./#../...
# .#./..#/### => #..#/..../..../#..#

# As before, the program begins with this pattern:

# .#.
# ..#
# ###

# The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square; the square matches the second rule, which produces:

# #..#
# ....
# ....
# #..#

# The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four squares:

# #.|.#
# ..|..
# --+--
# ..|..
# #.|.#

# Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation to line up with the rule. The output for the rule is the same in all four cases:

# ##.|##.
# #..|#..
# ...|...
# ---+---
# ##.|##.
# #..|#..
# ...|...

# Finally, the squares are joined into a new grid:

# ##.##.
# #..#..
# ......
# ##.##.
# #..#..
# ......

# Thus, after 2 iterations, the grid contains 12 pixels that are on.

# How many pixels stay on after 5 iterations?

with open('day21.txt') as puzzle_file:
    puzzle_input = puzzle_file.read().split('\n')

book_of_rules = {}

def add_rules(raw_rules):
    for rule in raw_rules:
        input_pattern = rule[0:rule.index(' ')]
        output_pattern = rule[rule.index('>') + 2:]
        book_of_rules[input_pattern] = output_pattern

add_rules(puzzle_input)

def flip(grid):
    grid = grid.split('/')
    grid[0], grid[-1] = grid[-1], grid[0]
    return '/'.join(grid)

def rotate(grid):
    grid = grid.split('/')
    if len(grid) == 2:
        new_grid = grid[1][0] + grid[0][0] + '/' + grid[1][1] + grid[0][1]
    elif len(grid) == 3:
        new_grid = grid[2][0] + grid[1][0] + grid[0][0] + '/' + grid[2][1] + grid[1][1] + grid[0][1] + '/' + grid[2][2] + grid[1][2] + grid[0][2]
    return new_grid

def find_match(rules, grid):
    transformations = [grid, flip(grid), rotate(grid), flip(rotate(grid)), rotate(rotate(grid)), flip(rotate(rotate(grid))), rotate(rotate(rotate(grid))), flip(rotate(rotate(rotate(grid))))]
    for transformation in transformations:
        if transformation in rules.keys():
            return transformation

def enhance(rules, grid):
    return rules[grid]

example = '#..#/..../..../#..#'
# ##.|##.
# #..|#..
# ...|...
# ---+---
# ##.|##.
# #..|#..
# ...|...

example_rules = {'../.#': '##./#../...',
'.#./..#/###': '#..#/..../..../#..#'}

def divide(rules, grid):
    grid = grid.split('/')
    vert_split_grid = []
    horizon_split_grid = []
    new_split_grid = []
    enhanced_grid = []
    final_grid = []
    if len(grid) % 2 == 0:
        for row in xrange(0, len(grid), 2):
            vert_split_grid.append(grid[row] + '/' + grid[row+1])
    if len(grid) % 3 == 0:
        for row in xrange(0, len(grid), 3):
            vert_split_grid.append(grid[row] + '/' + grid[row+1] + '/' + grid[row+2])
    vert_split_grid = [rows.split('/') for rows in vert_split_grid]
    if len(vert_split_grid) == 1:
        if len(vert_split_grid[0][0]) == 2:
            new_split_grid.append(vert_split_grid[0][0] + '/' + vert_split_grid[0][1])
        else:
            new_split_grid.append(vert_split_grid[0][0] + '/' + vert_split_grid[0][1] + '/' + vert_split_grid[0][2])
    if len(vert_split_grid) % 2 == 0:
        for pos in xrange(0, len(grid), 2):
            for rows in vert_split_grid:
                for row in rows:
                    horizon_split_grid.append(row[pos] + row[pos+1])
        for n in xrange(0, len(horizon_split_grid), 2):
            new_split_grid.append(horizon_split_grid[n] + '/' + horizon_split_grid[n+1])
    if len(vert_split_grid) % 3 == 0:
        for pos in xrange(0, len(grid), 3):
            for rows in vert_split_grid:
                for row in rows:
                    horizon_split_grid.append(row[pos] + row[pos+1] + row[pos+2])
        for n in xrange(0, len(horizon_split_grid), 3):
            new_split_grid.append(horizon_split_grid[n] + '/' + horizon_split_grid[n+1] + '/' + horizon_split_grid[n+2])
    for new_grid in new_split_grid:
        enhanced_grid.append(enhance(rules, find_match(rules, new_grid)))
    if len(enhanced_grid) > 1:
        enhanced_grid = [enhanced_grid[:len(enhanced_grid)/2], enhanced_grid[len(enhanced_grid)/2:]]
        for pos in xrange(0, len(enhanced_grid[0])):
            for grids in enhanced_grid:
                final_grid.append(grids[pos])
    else:
        final_grid = enhanced_grid
    return '/'.join(final_grid)

print divide(example_rules, example)
# print divide(book_of_rules, divide(book_of_rules, '.#./..#/###'))