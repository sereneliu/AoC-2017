# --- Day 23: Coprocessor Conflagration ---

# You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer, so you head in and see what you can do.

# The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality seems very similar, but some of the instructions are different:

# set X Y sets register X to the value of Y.
# sub X Y decreases register X by the value of Y.
# mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
# jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)

# Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

# The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any meaningful work.

# If you run the program (your puzzle input), how many times is the mul instruction invoked?

import sympy.ntheory.primetest

with open('day23.txt') as puzzle_file:
    puzzle_input = [line.split(' ') for line in puzzle_file.read().split('\n')]

register_dict = {}

def find_registers(instructions):
    for instruction in instructions:
        if instruction[1].isalpha():
            register_dict[instruction[1]] = 0

# def read_instructions(instructions):
#     find_registers(instructions)
#     mul_instruction = 0
#     i = 0
#     num = 0
#     while i < len(instructions):
#         instruction = instructions[i][0]
#         if instructions[i][1] not in register_dict.keys():
#             register = int(instructions[i][1])
#         else:
#             register = instructions[i][1]
#         if len(instructions[i]) > 2:
#             if instructions[i][2] not in register_dict.keys():
#                 num = int(instructions[i][2])
#             else:
#                 num = register_dict[instructions[i][2]]
#         if instruction == 'set':
#             register_dict[register] = num
#         if instruction == 'sub':
#             register_dict[register] -= num
#         if instruction == 'mul':
#             register_dict[register] *= num
#             mul_instruction += 1
#         if instruction == 'jnz' and register_dict.get(register, register) != 0:
#             i += num
#         else:
#             i += 1
#     return mul_instruction

# print read_instructions(puzzle_input)

def read_instructions(instructions, i, times_to_loop):
    for l in xrange(times_to_loop):
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
        if instruction == 'set':
            register_dict[register] = num
        if instruction == 'sub':
            register_dict[register] -= num
        if instruction == 'mul':
            register_dict[register] *= num
        if instruction == 'jnz' and register_dict.get(register, register) != 0:
            i += num
        else:
            i += 1

# set b 57              # set-up
# set c b
# jnz a 2
# jnz 1 5
# mul b 100
# sub b -100000         # b = 105,700
# set c b
# sub c -17000          # c = 122,700
#    set f 1            # f = 1
#    set d 2            # start d at 2
#        set e 2        # start e at 2
#            set g d
#            mul g e
#            sub g b
#            jnz g 2    # if d * e = b:
#            set f 0        # f = 0

#            sub e -1   # e += 1
#            set g e
#            sub g b    # if e = b:
#            jnz g -8       # end loop
#        sub d -1       # d += 1
#        set g d
#        sub g b        # if d = b:
#        jnz g -13          # end loop
#    jnz f 2            # if f = 0:
#    sub h -1               # h += 1
#    set g b
#    sub g c            # if b = c:
#    jnz g 2                # end loop
#    jnz 1 3            # else:
#    sub b -17              b += 17
#    jnz 1 -23

import sympy

def debug_mode(instructions):
    find_registers(instructions)
    register_dict['a'] = 1
    read_instructions(instructions, 0, 10)
    for b in xrange(register_dict['b'], register_dict['c'] + 1, 17):
        register_dict['f'] = 1
#        for d in xrange(2, register_dict['b'] + 1):
#           for e in xrange(2, register_dict['b'] + 1):
#               if register_dict['d'] * register_dict['e'] == register_dict['b']:
#                   register_dict['f'] = 0
        if not sympy.ntheory.primetest.isprime(b):
            register_dict['h'] += 1
    return register_dict['h']
    
print debug_mode(puzzle_input)



# assert register_dict['e'] != register_dict['b'], "loop: %s, %s" % (l, register_dict)
# AssertionError: loop: 422796, {'a': 1, 'c': 122700, 'b': 105700, 'e': 52850, 'd': 2, 'g': 0, 'f': 1, 'h': 0}
# AssertionError: loop: 845591, {'a': 1, 'c': 122700, 'b': 105700, 'e': 105700, 'd': 2, 'g': 105698, 'f': 0, 'h': 0}