# --- Day 18: Duet ---

# You discover a tablet containing some strange assembly code labeled simply "Duet". Rather than bother the sound card with it, you decide to run the code yourself. Unfortunately, you don't see any documentation, so you're left to figure out what the instructions mean on your own.

# It seems like the assembly is meant to operate on a set of registers that are each named with a single letter and that can each hold a single integer. You suppose each register should start with a value of 0.

# There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:

# snd X plays a sound with a frequency equal to the value of X.
# set X Y sets register X to the value of Y.
# add X Y increases register X by the value of Y.
# mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
# mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
# rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
# jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
# Many of the instructions can take either a register (a single letter) or a number. The value of a register is the integer it contains; the value of a number is that number.

# After each jump instruction, the program continues with the instruction to which the jump jumped. After any other instruction, the program continues with the next instruction. Continuing (or jumping) off either end of the program terminates it.

# For example:

test_input = '''set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2'''

# The first four instructions set a to 1, add 2 to it, square it, and then set it to itself modulo 5, resulting in a value of 4.
# Then, a sound with frequency 4 (the value of a) is played.
# After that, a is set to 0, causing the subsequent rcv and jgz instructions to both be skipped (rcv because a is 0, and jgz because a is not greater than 0).
# Finally, a is set to 1, causing the next jgz instruction to activate, jumping back two instructions to another jump, which jumps again to the rcv, which ultimately triggers the recover operation.
# At the time the recover operation is executed, the frequency of the last sound played is 4.

# What is the value of the recovered frequency (the value of the most recently played sound) the first time a rcv instruction is executed with a non-zero value?

test_input = [line.split(' ') for line in test_input.split('\n')]

puzzle_input = open('day18.txt', 'r')
puzzle_input = [line.split(' ') for line in puzzle_input.read().split('\n')]

register_dict = {}

def find_registers(instructions):
    for instruction in instructions:
        if instruction[1] in 'abcdefghijklmnopqrstuvwxyz':
            register_dict[instruction[1]] = 0

def read_instructions(instructions):
    find_registers(instructions)
    frequency = 0
    i = 0
    num = 0
    while i < len(instructions):
        instruction = instructions[i][0]
        if instructions[i][1] not in register_dict.keys():
            register = int(instructions[i][1])
        else:
            register = instructions[i][1]
        if len(instructions[i]) > 2:
            if instructions[i][2] not in register_dict.keys():
                num = int(instructions[i][2])
            else:
                num = register_dict[instructions[i][2]]
        if instruction == 'snd':
            frequency = register_dict[register]
        if instruction == 'set':
            register_dict[register] = num
        if instruction == 'add':
            register_dict[register] += num
        if instruction == 'mul':
            register_dict[register] *= num
        if instruction == 'mod':
            register_dict[register] %= num
        if register_dict[register] != 0:
            if instruction == 'jgz':
                i += num
            else:
                i += 1
            if instruction == 'rcv':
                return frequency
        else:
            i += 1

print read_instructions(puzzle_input) # answer: 7071