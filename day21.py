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

example = '#..#/..../..../#..#'

example_rules = {'../.#': '##./#../...',
'.#./..#/###': '#..#/..../..../#..#'}

import math

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

def divide(rules, grid):
    grid = grid.split('/')
    skip = 0
    new_grids = []
    formatted_new_grids = []
    if len(grid) % 2 == 0:
        skip = 2
    elif len(grid) % 3 == 0:
        skip = 3
    for rows in xrange(0, len(grid), skip):
        for pos in xrange(0, len(grid), skip):
            for row in xrange(len(grid[rows:rows+skip])):
                new_grids.append(grid[rows:rows+skip][row][pos:pos+skip])
    for pos in xrange(0, len(new_grids), skip):
        new_grid = []
        for n in xrange(0, skip):
            new_grid.append(new_grids[pos+n])
        formatted_new_grids.append('/'.join(new_grid))
    return formatted_new_grids

def enhanced_grid(rules, grid):
    enhanced_grid = []
    for new_grid in divide(rules, grid):
        enhanced_grid.append(enhance(rules, find_match(rules, new_grid)))
    return enhanced_grid

def join_grid(grids):
    split_grids = []
    reorder_grid = []
    final_grid = []
    for grid in grids:
        grid = grid.split('/')
        split_grids.append(grid)
    side_len = int(math.sqrt(len(split_grids)))
    for rows in xrange(0, len(split_grids), side_len):
        for pos in xrange(0, len(split_grids[rows])):
            for row in xrange(rows, rows + side_len):
                reorder_grid.append(split_grids[row][pos])
    combine_row = []
    for pos in xrange(0, len(reorder_grid), side_len):
        combine_row.append(reorder_grid[pos:pos+side_len])
    for row in combine_row:
        final_grid.append(''.join(row))
    final_grid = '/'.join(final_grid)
    return final_grid

def iterations(rules, grid, num):
    end_grid = join_grid(enhanced_grid(rules, grid))
    if num > 1:
        num -= 1
        end_grid = iterations(rules, end_grid, num)
    return end_grid

# print iterations(example_rules, '.#./..#/###', 2).count('#')
# print iterations(book_of_rules, '.#./..#/###', 5).count('#')

# --- Part Two ---
# How many pixels stay on after 18 iterations?

print iterations(book_of_rules, '.#./..#/###', 18).count('#')