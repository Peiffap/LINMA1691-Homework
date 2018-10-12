"""
    Students template for the second homework of LINMA1691 "Théorie des graphes".

    Authors : Devillez Henri
"""


import queue as Q
from collections import deque

# You cannot import other modules
# You do not have to use all imported modules


def shortest_path_1(maze):
    """ 
    INPUT : 
        - maze, a 2D array representing the maze    
    OUTPUT :
        - return the minimal number of steps required to go to the exit of the maze.
        
        See project statement for more details
    """

    wall, clear, goal = "#", ".", "E"
    height = len(maze)
    width = len(maze[0])

    def find_start(grid):
        for y in range(1, len(grid)-1):
            for x in range(1, len(grid[0])-1):
                if grid[y][x] == 'S':
                    return tuple([x, y])

    start = find_start(maze)

    queue = deque([[start]])

    seen = {start}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if maze[y][x] == goal:
            return len(path)-1
        for (x2, y2) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 < x2 < width-1 and 0 < y2 < height-1 and maze[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

    return -1


def shortest_path_2(tasks, paths):
    """ 
    INPUT : 
        - tasks, the time to achieve each task (in minutes)
        - paths, list of tuples (a, b, t) giving a trail between tasks a and b.
          You need t minutes to walk this trail.
    OUTPUT :
        - return the time you need to finish the game
          
        See project statement for more details
    """

    return -1


if __name__ == "__main__":

    # Read Input for the first exercise

    with open('in1.txt', 'r') as fd:
        l = fd.readline()
        l = l.split(' ')

        n = int(l[0])
        m = int(l[1])

        maze = []
        for row in range(n):
            l = fd.readline().rstrip()
            maze.append(list(l))

    # Compute answer for the first exercise

    ans1 = shortest_path_1(maze)

    # Check results for the first exercise

    with open('out1.txt', 'r') as fd:
        l_output = fd.readline()
        expected_output = int(l_output)

        if expected_output == ans1:
            print("Exercice 1 : Correct")
        else:
            print("Exercice 1 : Wrong answer")
            print("Your output : %d ; Correct answer : %d" % (ans1, expected_output))

            # Read Input for the second exercise

    with open('in2.txt', 'r') as fd:
        l = fd.readline().split(' ')

        n = int(l[0])
        m = int(l[1])

        tasks = [int(x) for x in fd.readline().rstrip().split(' ')]

        paths = []
        for p in range(n):
            l = fd.readline().rstrip().split(' ')
            paths.append(tuple([int(x) for x in l]))

    # Compute answer for the second exercise

    ans2 = shortest_path_2(tasks, paths)

    # Check results for the second exercise

    with open('out2.txt', 'r') as fd:
        l_output = fd.readline()
        expected_output = int(l_output)

        if expected_output == ans2:
            print("Exercice 2 : Correct")
        else:
            print("Exercice 2 : Wrong answer")
            print("Your output : %d ; Correct answer : %d" % (ans2, expected_output))
