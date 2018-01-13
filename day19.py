# --- Day 19: A Series of Tubes ---

# Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but it's confused about where to go.

# Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take, starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it reaches the end (located somewhere within the diagram) and stop there.

# Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn left or right when there's no other option. In addition, someone has left letters on the line; these also don't change its direction, but it can use them to keep track of where it's been. For example:

#     |          
#     |  +--+    
#     A  |  C    
# F---|----E|--+ 
#     |  |  |  D 
#     +B-+  +--+ 

# Given this diagram, the packet needs to take the following path:

# Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to the first +.
# Travel right, up, and right, passing through B in the process.
# Continue down (collecting C), right, and up (collecting D).
# Finally, go all the way left through E and stopping at F.
# Following the path to the end, the letters it sees on its path are ABCDEF.

# The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

with open('day19.txt') as puzzle_file:
    puzzle_input = list(puzzle_file)

def down(x, y):
     return x, y + 1

def up(x, y):
     return x, y - 1
     
def right(x, y):
     return x + 1, y

def left(x, y):
     return x - 1, y

directions = {
     'down': down,
     'up': up,
     'right': right,
     'left': left
}

def find_the_way(maze):
     collection = []
     direction = 'down'
     y = 0
     x = maze[y].index('|')
     steps = 0
     while 0 <= y < len(maze) and 0 <= x < len(maze[y]) and (maze[y][x].isalpha() or maze[y][x] in '|-+'):
          if maze[y][x].isalpha():
               collection.append(maze[y][x])
          if maze[y][x] == '+':
               if direction in ('down', 'up'):
                    if x < len(maze[y]) - 1 and maze[y][x + 1] != ' ':
                              direction = 'right'
                    elif x > 0 and maze[y][x - 1] != ' ':
                              direction = 'left'
               elif direction in ('right', 'left'):
                    if y < len(maze) - 1 and maze[y + 1][x] != ' ':
                              direction = 'down'
                    elif y > 0 and maze[y - 1][x] != ' ':
                              direction = 'up'
          x, y = directions[direction](x, y)
          steps += 1
     return ''.join(collection), steps
          
print find_the_way(puzzle_input) # answer: ('SXWAIBUZY', 16676)