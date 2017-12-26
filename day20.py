from __future__ import print_function
from collections import defaultdict, namedtuple
import sys

if sys.version_info >= (3, 0):
    xrange = range

# --- Day 20: Particle Swarm ---

# Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.

# It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

# Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

# Increase the X velocity by the X acceleration.
# Increase the Y velocity by the Y acceleration.
# Increase the Z velocity by the Z acceleration.
# Increase the X position by the X velocity.
# Increase the Y position by the Y velocity.
# Increase the Z position by the Z velocity.

# Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

# For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity). Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current X positions (marked in parenthesis), the following would take place:

# p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

# p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

# p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

# p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   

# At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will stay closest.

# Which particle will stay closest to position <0,0,0> in the long term?

Vector = namedtuple('Vector', ('x', 'y', 'z'))
Point = namedtuple('Point', ('position', 'velocity', 'acceleration'))

def parse_vector(str):
    begin = str.index('<') + 1
    end = str.index('>', begin)
    x, y, z = str[begin:end].split(',')
    return Vector(int(x), int(y), int(z))

def add_vector(a, b):
    x, y, z = a
    u, v, w = b
    return Vector(x + u, y + v, z + w)

def step(point):
    position, velocity, acceleration = point
    velocity = add_vector(velocity, acceleration)
    position = add_vector(position, velocity)
    return Point(position, velocity, acceleration)

input_points = []
with open('day20.txt') as puzzle_file:
    for line in puzzle_file:
        position, velocity, acceleration = line.split()
        input_points.append(Point(
            parse_vector(position),
            parse_vector(velocity),
            parse_vector(acceleration)))

points = list(input_points)
for _ in xrange(400):
    closest_distance = float('inf')
    for i in range(len(points)):
        points[i] = step(points[i])
        x, y, z = points[i].position
        distance = abs(x) + abs(y) + abs(z)
        if distance < closest_distance:
            closest_index, closest_distance = i, distance
print(closest_index)

# --- Part Two ---

# To simplify the problem further, the GPU would like to remove any particles that collide. Particles collide if their positions ever exactly match. Because particles are updated simultaneously, more than two particles can collide at the same time and place. Once particles collide, they are removed and cannot collide with anything else after that tick.

# For example:

# p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
# p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
# p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
# p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

# p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
# p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
# p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
# p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

# p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
# p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
# p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
# p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

# ------destroyed by collision------    
# ------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
# ------destroyed by collision------                      (3)         
# p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

# In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X. On the next tick, particle 3 passes through unharmed.

# How many particles are left after all collisions are resolved?

points = list(input_points)
for _ in xrange(40):
    positions = defaultdict(int)
    for i in range(len(points)):
        points[i] = step(points[i])
        positions[points[i].position] += 1
    points = [point for point in points if positions[point.position] == 1]
print(len(points))
