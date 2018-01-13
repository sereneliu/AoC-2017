# --- Day 8: I Heard You Like Registers ---

# You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions.

# Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0. The instructions look like this:

# b inc 5 if a > 1
# a inc 1 if b < 5
# c dec -10 if a >= 1
# c inc -20 if c == 10
# These instructions would be processed as follows:

# Because a starts at 0, it is not greater than 1, and so b is not modified.
# a is increased by 1 (to 1) because b is less than 5 (it is 0).
# c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
# c is increased by -20 (to -10) because c is equal to 10.
# After this process, the largest value in any register is 1.

# You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

# What is the largest value in any register after completing the instructions in your puzzle input?

# --- Part Two ---

# To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide how much memory to allocate to these operations. For example, in the above instructions, the highest value ever held was 10 (in register c after the third instruction was evaluated).

test_instructions = '''b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10'''

with open('day8.txt') as puzzle_file:
    puzzle_input = puzzle_file.read().split('\n')

registers = set()
reg_values = {}

def setup(some_list):
    for instruction in some_list:
        i = some_list.index(instruction)
        instruction = instruction.split()
        register = instruction[0]
        registers.add(register)
        instruction[0] = 'reg_values["' + register + '"]'
        register_2 = instruction[4]
        instruction[4] = 'reg_values["' + register_2 + '"]'
        if instruction[1] == 'inc':
            instruction[1] = '+='
        if instruction[1] == 'dec':
            instruction[1] = '-='
        instruction = ' '.join(instruction)
        some_list[i] = instruction
    for register in registers:
        reg_values.update({register: 0})

def run_instructions(some_list):
    setup(some_list)
    max_value_ever = 0
    for instruction in some_list:
        if eval(instruction[instruction.index(' if') + 4:]) == True:
            exec(instruction[0:instruction.index(' if') + 1])
            if max(reg_values.values()) > max_value_ever:
                max_value_ever = max(reg_values.values())
    return max(reg_values.values()), max_value_ever

print run_instructions(puzzle_input) # (4902, 7037)