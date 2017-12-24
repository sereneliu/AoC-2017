from __future__ import print_function
import operator


def max_bridge(parts, start, cur=0, add=operator.add):
    max_val = cur
    for i, (a, b) in enumerate(parts):
        if a == start:
            pass
        elif b == start:
            a, b = b, a
        else:
            continue
        new_parts = parts[:i] + parts[i + 1:]
        weight = a + b
        max_val = max(max_val,
                      max_bridge(
                          new_parts, start=b, cur=add(weight, cur), add=add))
    return max_val


def part1(parts):
    """
    >>> part1([(0,2),(2,2),(2,3),(3,4),(3,5),(0,1),(10,1),(9,10)])
    31
    """
    return max_bridge(parts, start=0)


def part2(parts):
    """
    >>> part2([(0,2),(2,2),(2,3),(3,4),(3,5),(0,1),(10,1),(9,10)])
    19
    """

    def add(weight, val):
        cur_length, cur_weight = val
        return (cur_length + 1, cur_weight + weight)

    max_len, weight = max_bridge(parts, start=0, cur=(0, 0), add=add)
    return weight


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    puzzle_input = []
    with open('day24.txt') as puzzle_file:
        for line in puzzle_file:
            a, b = line.strip().split('/')
            puzzle_input.append((int(a), int(b)))

    print('Part 1:', part1(puzzle_input))
    print('Part 2:', part2(puzzle_input))
