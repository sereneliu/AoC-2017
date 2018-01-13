# --- Day 16: Permutation Promenade ---

# You come upon a very unusual sight; a group of programs here appear to be dancing.

# There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b stands in position 1, and so on until p, which stands in position 15.

# The programs' dance consists of a sequence of dance moves:

# Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
# Exchange, written xA/B, makes the programs at positions A and B swap places.
# Partner, written pA/B, makes the programs named A and B swap places.
# For example, with only five programs standing in a line (abcde), they could do the following dance:

# s1, a spin of size 1: eabcd.
# x3/4, swapping the last two programs: eabdc.
# pe/b, swapping programs e and b: baedc.
# After finishing their dance, the programs end up in order baedc.

# You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs standing after their dance?

test_programs = 'abcde'
test_input = 's1,x3/4,pe/b'.split(',')

puzzle_programs = 'abcdefghijklmnop'
with open('day16.txt') as puzzle_file:
    puzzle_input = puzzle_file.read().split(',')

def spin(size, programs):
    programs = programs[-1 * size:] + programs[0:-1 * size]
    return programs

def exchange(pos_a, pos_b, programs):
    a = min(pos_a, pos_b)
    b = max(pos_a, pos_b)
    programs = programs[0:a] + programs[b] + programs[a + 1:b] + programs[a] + programs[b + 1:]
    return programs

def partner(prog_a, prog_b, programs):
    a = min(programs.index(prog_a), programs.index(prog_b))
    b = max(programs.index(prog_a), programs.index(prog_b))
    programs = programs[0:a] + programs[b] + programs[a + 1:b] + programs[a] + programs[b + 1:]
    return programs

def dance_moves(programs, instructions):
    for instruction in instructions:
        if instruction[0] == 's':
            programs = spin(int(instruction[1:]), programs)
        if instruction[0] == 'x':
            programs = exchange(int(instruction[1:instruction.index('/')]), int(instruction[instruction.index('/') + 1:]), programs)
        if instruction[0] == 'p':
            programs = partner(instruction[1:instruction.index('/')], instruction[instruction.index('/') + 1:], programs)
    return programs

# print dance_moves(puzzle_programs, puzzle_input) # answer: iabmedjhclofgknp

# --- Part Two ---

# Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

# Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the first dance, a total of one billion (1000000000) times.

# In the example above, their second dance would begin with the order baedc, and use the same dance moves:

# s1, a spin of size 1: cbaed.
# x3/4, swapping the last two programs: cbade.
# pe/b, swapping programs e and b: ceadb.

# In what order are the programs standing after their billion dances?

def billion_dances(programs, instructions):
    seen = []
    for n in range(1000000000):
        if programs not in seen:
            seen.append(programs)
            programs = dance_moves(programs, instructions)
        else:
            return seen[1000000000 % len(seen)]

print billion_dances(puzzle_programs, puzzle_input)