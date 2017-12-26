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

# test_coordinates = [[3, 2, 1], [2, 1, 0], [1, 2, 3]]

import sys

with open('day20.txt') as puzzle_file:
    puzzle_input = list(puzzle_file)

particle_dict = {}

def add_to_particle_dict(some_input):
    num = 0
    for particle in some_input:
        particle = ''.join(c for c in particle if (c.isdigit()) or c in '-,')
        particle = [int(coordinate) for coordinate in particle.split(',')]
        particle_dict['particle ' + str(num)] = [[particle[0], particle[1], particle[2]], [particle[3], particle[4], particle[5]], [particle[6], particle[7], particle[8]]]
        num += 1

add_to_particle_dict(puzzle_input)

def update_particles(dictionary):
    for coordinates in dictionary.values():
        coordinates[1][0] += coordinates[2][0]
        coordinates[1][1] += coordinates[2][1]
        coordinates[1][2] += coordinates[2][2]
        coordinates[0][0] += coordinates[1][0]
        coordinates[0][1] += coordinates[1][1]
        coordinates[0][2] += coordinates[1][2]

def manh_dist(coordinates):
    return sum(abs(coordinate) for coordinate in coordinates[0])
    
closest_to_zero = []

def save_min(dictionary):
    min_part = ''
    min_dist = sys.maxint
    for name, coordinates in dictionary.items():
        min_dist = min(manh_dist(coordinates), min_dist)
        if min_dist == manh_dist(coordinates):
            min_part = name
    closest_to_zero.append(min_part)
    
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

def remove_collisions(dictionary):
    positions = []
    particle_collision = []
    for particle, coordinates in dictionary.items():
        positions.append(coordinates[0])
    for coordinate in positions:
        if positions.count(coordinate) > 1:
            particle_collision.append(coordinate)
    for particle, coordinates in dictionary.items():
        if coordinates[0] in particle_collision:
            del dictionary[particle]

def long_run(dictionary, runs):
    for _ in xrange(runs):
        save_min(dictionary)
        update_particles(dictionary)
        remove_collisions(dictionary)
                    
long_run(particle_dict, 1000)
#print max(set(closest_to_zero), key=closest_to_zero.count)
print len(particle_dict)