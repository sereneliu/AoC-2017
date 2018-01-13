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

# def horizontal_flip(grid):
#    grid = grid.split('/')
#    new_grid = []
#    for line in grid:
#        line = list(line)
#        line[0], line[-1] = line[-1], line[0]
#        new_grid.append(''.join(line))
#    return '/'.join(new_grid)

def rotate(grid):
    grid = grid.split('/')
    if len(grid) == 2:
        new_grid = grid[1][0] + grid[0][0] + '/' + grid[1][1] + grid[0][1]
    elif len(grid) == 3:
        new_grid = grid[2][0] + grid[1][0] + grid[0][0] + '/' + grid[2][1] + grid[1][1] + grid[0][1] + '/' + grid[2][2] + grid[1][2] + grid[0][2]
    return new_grid

def find_match(grid):
    if grid not in book_of_rules.keys():
        if flip(grid) not in book_of_rules.keys():
            if rotate(grid) not in book_of_rules.keys():
                if flip(rotate(grid)) not in book_of_rules.keys():
                    if rotate(rotate(grid)) not in book_of_rules.keys():
                        if flip(rotate(rotate(grid))) not in book_of_rules.keys():
                            if rotate(rotate(rotate(grid))) not in book_of_rules.keys():
                                grid = flip(rotate(rotate(rotate(grid))))
                            else:
                                grid = rotate(rotate(rotate(grid)))
                        else:
                            grid = flip(rotate(rotate(grid)))
                    else:
                        grid = rotate(rotate(grid))
                else:
                    grid = flip(rotate(grid))
            else:
               grid = rotate(grid) 
        else: 
            grid = flip(grid)
    return grid

example = '#..#/..../..../#..#'
# ##.|##.
# #..|#..
# ...|...
# ---+---
# ##.|##.
# #..|#..
# ...|...

def divide(grid):
    grid = grid.split('/')
    new_grids = []
    for row in grid:
        if len(row) % 2 == 0:
            for x in xrange(0, len(row), 2):
                new_grids.append(row[x] + row[x+1])
        if len(row) % 3 == 0:
            for x in xrange(0, len(row), 3):
                new_grids.append(row[x] + row[x+1] + row[x+2])
    return new_grids

print divide(example)

def enhance(grid):
    return book_of_rules[grid]

def iterate(grid):
    return enhance(find_match(grid))

print iterate('.#./..#/###')
# print '.#./..#/###'
# print '.#./..#/###' in book_of_rules.keys()
# print flip('.#./..#/###')
# print flip('.#./..#/###') in book_of_rules.keys()
# print rotate('.#./..#/###')
# print rotate('.#./..#/###') in book_of_rules.keys()
# print flip(rotate('.#./..#/###'))
# print flip(rotate('.#./..#/###')) in book_of_rules.keys()
# print rotate(rotate('.#./..#/###'))
# print rotate(rotate('.#./..#/###')) in book_of_rules.keys()
# print flip(rotate(rotate('.#./..#/###')))
# print flip(rotate(rotate('.#./..#/###'))) in book_of_rules.keys()
# print rotate(rotate(rotate('.#./..#/###')))
# print rotate(rotate(rotate('.#./..#/###'))) in book_of_rules.keys()
# print flip(rotate(rotate(rotate('.#./..#/###'))))
# print flip(rotate(rotate(rotate('.#./..#/###')))) in book_of_rules.keys()

# original
# 12
# 34

# vertical flip
# 21
# 43

# rotate
# 24
# 13

# flip rotate
# 42
# 31

# rotate x2
# 43
# 21

# flip rotate x2 // horizontal flip
# 34
# 12

# rotate x3
# 31
# 42

# flip rotate x3
# 13
# 24

# from Daniel
# 21
# 34

# 43
# 12

# 14
# 23

# 32
# 41