# --- Day 7: Recursive Circus ---
# Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large tower.

# One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced several more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs, each holding their own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping the disc below them balanced but with no disc of their own.

# You offer to help, but first you need to understand the structure of these towers. You ask each program to yell out their name, their weight, and (if they're holding a disc) the names of the programs immediately above them balancing on that disc. You write this information down (your puzzle input). Unfortunately, in their panic, they don't do this in an orderly fashion; by the time you're done, you're not sure which program gave which information.

# For example, if your list is the following:

# pbga (66)
# xhth (57)
# ebii (61)
# havc (66)
# ktlj (57)
# fwft (72) -> ktlj, cntj, xhth
# qoyq (66)
# padx (45) -> pbga, havc, qoyq
# tknk (41) -> ugml, padx, fwft
# jptl (61)
# ugml (68) -> gyxo, ebii, jptl
# gyxo (61)
# cntj (57)
# ...then you would be able to recreate the structure of the towers that looks like this:

#                gyxo
#              /     
#         ugml - ebii
#       /      \     
#      |         jptl
#      |        
#      |         pbga
#     /        /
#tknk --- padx - havc
#     \        \
#      |         goyq
#      |             
#      |         ktlj
#       \      /     
#         fwft - cntj
#              \     
#                xhth
# In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx, and fwft. Those programs are, in turn, holding up other programs; in this example, none of those programs are holding up any other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is much larger.)

# Before you're ready to help them, you need to make sure your information is correct. What is the name of the bottom program?

puzzle_input = open("day7_test.txt", "r")
puzzle_input = puzzle_input.read()
input_list = puzzle_input.split("\n")

towers = {}

def tower_dict(some_input):
    for line in some_input:
        tower_name = line[0:line.index(" ")]
        holding_up = []
        if "-> " in line:
            holding_up = [(line[line.index("(") + 1:line.index(")")])] + line[line.index("-> ") + 3:].split(", ")
        else:
            holding_up = [(line[line.index("(") + 1:line.index(")")])]
        towers.update({tower_name: holding_up})
    return towers

def bottom_tower(some_input):
    all_towers = set()
    sub_towers = set()
    for tower, sub_tower in tower_dict(input_list).items():
        all_towers.add(tower)
        sub_towers.update(sub_tower[1:])
    return (all_towers.difference(sub_towers))

print bottom_tower(input_list) # answer: tknk

# --- Part Two ---

# The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's fixed, they're stuck here.

# For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers are supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum of the weights of the programs in that tower.

# In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have the same weight, and they do: 61.

# However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each match. This means that the following sums must all be the same:

# ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
# padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
# fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243
# As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the nodes above ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the towers balanced. If this change were made, its weight would be 60.

# Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?

def balance_towers_above(some_input):
    sub_towers = towers[bottom_tower(some_input).pop()][1:]
    tower_weights = {}
    for sub_tower in sub_towers:
        def stack_weight(some_towers, weight):
            for some_tower in some_towers:
                weight += (int(towers[some_tower][0]))
                if len(towers[some_tower]) > 1:
                    print (towers[sub_tower][1:], weight)
                    stack_weight(towers[sub_tower][1:], weight)
            return weight
        tower_weights[sub_tower] = stack_weight(towers[sub_tower][1:], int(towers[sub_tower][0]))
    print tower_weights
    unique_weights = set()
    for value in tower_weights.values():
        unique_weights.add(value)
    unique_weights = list(unique_weights)
    return abs(unique_weights[1] - unique_weights[0])
    
# print balance_towers_above(input_list)