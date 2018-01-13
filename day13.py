# --- Day 13: Packet Scanners ---

# You need to cross a vast firewall. The firewall consists of several layers, each with a security scanner that moves back and forth across the layer. To succeed, you must not be detected by a scanner.

# By studying the firewall briefly, you are able to record (in your puzzle input) the depth of each layer and the range of the scanning area for the scanner within it, written as depth: range. Each layer has a thickness of exactly 1. A layer at depth 0 begins immediately inside the firewall; a layer at depth 1 would start immediately after that.

# For example, suppose you've recorded the following:

# 0: 3
# 1: 2
# 4: 4
# 6: 4

# This means that there is a layer immediately inside the firewall (with range 3), a second layer immediately after that (with range 2), a third layer which begins at depth 4 (with range 4), and a fourth layer which begins at depth 6 (also with range 4). Visually, it might look like this:

#  0   1   2   3   4   5   6
# [ ] [ ] ... ... [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]
# Within each layer, a security scanner moves back and forth within its range. Each security scanner starts at the top and moves down until it reaches the bottom, then moves up until it reaches the top, and repeats. A security scanner takes one picosecond to move one step. Drawing scanners as S, the first few picoseconds look like this:


# Picosecond 0:
#  0   1   2   3   4   5   6
# [S] [S] ... ... [S] ... [S]
# [ ] [ ]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# Picosecond 1:
#  0   1   2   3   4   5   6
# [ ] [ ] ... ... [ ] ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# Picosecond 2:
#  0   1   2   3   4   5   6
# [ ] [S] ... ... [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [S]             [S]     [S]
#                 [ ]     [ ]

# Picosecond 3:
#  0   1   2   3   4   5   6
# [ ] [ ] ... ... [ ] ... [ ]
# [S] [S]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [S]     [S]

# Your plan is to hitch a ride on a packet about to move through the firewall. The packet will travel along the top of each layer, and it moves at one layer per picosecond. Each picosecond, the packet moves one layer forward (its first move takes it into layer 0), and then the scanners move one step. If there is a scanner at the top of the layer as your packet enters it, you are caught. (If a scanner moves into the top of its layer while you are there, you are not caught: it doesn't have time to notice you before you leave.) If you were to do this in the configuration above, marking your current position with parentheses, your passage through the firewall would look like this:

# Initial state:
#  0   1   2   3   4   5   6
# [S] [S] ... ... [S] ... [S]
# [ ] [ ]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# Picosecond 0:
#  0   1   2   3   4   5   6
# (S) [S] ... ... [S] ... [S]
# [ ] [ ]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# ( ) [ ] ... ... [ ] ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]


# Picosecond 1:
#  0   1   2   3   4   5   6
# [ ] ( ) ... ... [ ] ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] (S) ... ... [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [S]             [S]     [S]
#                 [ ]     [ ]


# Picosecond 2:
#  0   1   2   3   4   5   6
# [ ] [S] (.) ... [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [S]             [S]     [S]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [ ] (.) ... [ ] ... [ ]
# [S] [S]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [S]     [S]


# Picosecond 3:
#  0   1   2   3   4   5   6
# [ ] [ ] ... (.) [ ] ... [ ]
# [S] [S]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [S]     [S]

#  0   1   2   3   4   5   6
# [S] [S] ... (.) [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [ ]             [S]     [S]
#                 [ ]     [ ]


# Picosecond 4:
#  0   1   2   3   4   5   6
# [S] [S] ... ... ( ) ... [ ]
# [ ] [ ]         [ ]     [ ]
# [ ]             [S]     [S]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [ ] ... ... ( ) ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]


# Picosecond 5:
#  0   1   2   3   4   5   6
# [ ] [ ] ... ... [ ] (.) [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [S] ... ... [S] (.) [S]
# [ ] [ ]         [ ]     [ ]
# [S]             [ ]     [ ]
#                 [ ]     [ ]


# Picosecond 6:
#  0   1   2   3   4   5   6
# [ ] [S] ... ... [S] ... (S)
# [ ] [ ]         [ ]     [ ]
# [S]             [ ]     [ ]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [ ] ... ... [ ] ... ( )
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# In this situation, you are caught in layers 0 and 6, because your packet entered the layer when its scanner was at the top when you entered it. You are not caught in layer 1, since the scanner moved into the top of the layer once you were already there.

# The severity of getting caught on a layer is equal to its depth multiplied by its range. (Ignore layers in which you do not get caught.) The severity of the whole trip is the sum of these values. In the example above, the trip severity is 0*3 + 6*4 = 24.

# Given the details of the firewall you've recorded, if you leave immediately, what is the severity of your whole trip?

# --- Part Two ---

# Now, you need to pass through the firewall without being caught - easier said than done.

# You can't control the speed of the packet, but you can delay it any number of picoseconds. For each picosecond you delay the packet before beginning your trip, all security scanners move one step. You're not in the firewall during this time; you don't enter layer 0 until you stop delaying the packet.

# In the example above, if you delay 10 picoseconds (picoseconds 0 - 9), you won't get caught:

# State after delaying:
#  0   1   2   3   4   5   6
# [ ] [S] ... ... [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [S]             [S]     [S]
#                 [ ]     [ ]

# Picosecond 10:
#  0   1   2   3   4   5   6
# ( ) [S] ... ... [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [S]             [S]     [S]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# ( ) [ ] ... ... [ ] ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# Picosecond 11:
#  0   1   2   3   4   5   6
# [ ] ( ) ... ... [ ] ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [S] (S) ... ... [S] ... [S]
# [ ] [ ]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# Picosecond 12:
#  0   1   2   3   4   5   6
# [S] [S] (.) ... [S] ... [S]
# [ ] [ ]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [ ] (.) ... [ ] ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# Picosecond 13:
#  0   1   2   3   4   5   6
# [ ] [ ] ... (.) [ ] ... [ ]
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [S] ... (.) [ ] ... [ ]
# [ ] [ ]         [ ]     [ ]
# [S]             [S]     [S]
#                 [ ]     [ ]

# Picosecond 14:
#  0   1   2   3   4   5   6
# [ ] [S] ... ... ( ) ... [ ]
# [ ] [ ]         [ ]     [ ]
# [S]             [S]     [S]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [ ] ... ... ( ) ... [ ]
# [S] [S]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [S]     [S]

# Picosecond 15:
#  0   1   2   3   4   5   6
# [ ] [ ] ... ... [ ] (.) [ ]
# [S] [S]         [ ]     [ ]
# [ ]             [ ]     [ ]
#                 [S]     [S]

#  0   1   2   3   4   5   6
# [S] [S] ... ... [ ] (.) [ ]
# [ ] [ ]         [ ]     [ ]
# [ ]             [S]     [S]
#                 [ ]     [ ]

# Picosecond 16:
#  0   1   2   3   4   5   6
# [S] [S] ... ... [ ] ... ( )
# [ ] [ ]         [ ]     [ ]
# [ ]             [S]     [S]
#                 [ ]     [ ]

#  0   1   2   3   4   5   6
# [ ] [ ] ... ... [ ] ... ( )
# [S] [S]         [S]     [S]
# [ ]             [ ]     [ ]
#                 [ ]     [ ]

# Because all smaller delays would get you caught, the fewest number of picoseconds you would need to delay to get through safely is 10.

# What is the fewest number of picoseconds that you need to delay the packet to pass through the firewall without being caught?

test_input = '''0: 3
1: 2
4: 4
6: 4'''

test_input = test_input.split('\n')

with open('day13.txt') as puzzle_file:
    puzzle_input = puzzle_file.read().split('\n')

firewall_dict = {}

def setup_firewall(some_input):
    for layer in some_input:
        firewall_dict[int(layer[0:layer.index(':')])] = int(layer[layer.index(' ') + 1:])
    final_layer = max(firewall_dict.keys())
    firewall = []
    for n in range(final_layer + 1):
        firewall.append([])
    for f_depth, f_range in firewall_dict.items():
        for n in range(f_range):
            firewall[f_depth].append([n])
    return firewall

scanner_dict = {}

def scanners(dictionary):
    for key, value in dictionary.items():
        if value != []:
            scanner_cycle = []
            for n in range(int(value)):
                scanner_cycle.append(str(key) + '-' + str(n))
            for n in range(int(value))[::-1][1:-1]:
                scanner_cycle.append(str(key) + '-' + str(n))
        scanner_dict[key] = scanner_cycle
    return scanner_dict

def move_through_firewall(firewall, dictionary, delay):
#    caught = []
    i = 0
    for picosecond in range(len(firewall)):
        packet = str(i) + '-' + str(0)
        for scanner in scanners(dictionary).values():
            if packet == scanner[(i + delay) % len(scanner)]:
                return "caught"
#                caught.append(i)
        i += 1
#    severity = 0
#    for layer in caught:
#        severity += layer * firewall_dict[layer]
#    return severity
#    return caught

# print move_through_firewall(setup_firewall(puzzle_input), firewall_dict, 0) # answer: 648

def not_caught(firewall, dictionary):
    delay = 0
    caught = "caught"
    while caught == "caught":
        caught = move_through_firewall(firewall, dictionary, delay)
        delay += 1
    return delay - 1
        
print not_caught(setup_firewall(puzzle_input), firewall_dict) # answer: 3933124