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
    paths[1] = tuple((1,2,10))
    paths[0] = tuple((2,1,1))
    print(paths)
    print(tasks)
    
    # Return the lowest positive value of v
    def indexMin(v):
        index = -1
        found = 0
        for i in range(1,len(v)):
            if v[i] > -1:
                if found == 0:
                    res = v[i]
                    index = i
                    found = 1
                else:
                    if v[i] < res:
                        res = v[i]
                        index = i
        if found == 0:
            index = -1
        return index
    
    # Number of tasks
    N = len(tasks)
    A = []   
    # List des meilleurs chemins
    best = []
    tab  = []
    #N = 4
    # Initialiazing of A tab and best
    for i in range(0, N):        
        A.append([])
        tab.append([])
        best.append(0)
        for j in range(0, N):                           
                A[i].append(-1)
                tab[i].append(0)
    
            
    # Computation oh the weight of each arete            
    for i in range(0, len(paths)):
        if (A[paths[i][0]-1][paths[i][1]-1] == -1):
            A[paths[i][0]-1][paths[i][1]-1] = paths[i][2] + tasks[paths[i][1]-1]
        else:
            A[paths[i][0]-1][paths[i][1]-1] = min(A[paths[i][0]-1][paths[i][1]-1], paths[i][2] + tasks[paths[i][1]-1])
                
    
    #print(A)
    #A = [[-1, 10, -1, -1, 2, -1],[-1, -1, 2, -1, -1, 10],[-1, -1, -1, -1, -1, 2],[-1, 2, -1, -1, -1, 10],[-1, -1, -1, 2, -1, -1],[-1, -1, -1, -1, -1, -1]]
    #A = [[-1,2,2,-1],[-1,-1,-1,10],[-1,-1,-1,1],[-1,-1,-1,-1]]
    #print("\nA = {}\n".format(A))
    #N = 6
    # Dijkstra
    for i in range(0, N):
        tab[0][i] = A[0][i]
    tab[0][0] = -2
       
    current_node = indexMin(tab[0])
    current_weight = A[0][current_node]
    best[0] = 0
    best[current_node] = current_weight
    tab[0][current_node] = -2

    for i in range(1, N):
        
        for j in range(0, N):

            if tab[i-1][j] == -2: #deja defini best
                tab[i][j] = -2
            elif tab[i-1][j] == -1: #inf
                if A[current_node][j] == -1:
                    tab[i][j] = -1
                else:
                    tab[i][j] = A[current_node][j] + current_weight
            else:

                if A[current_node][j] == -1:
                    tab[i][j] = tab[i-1][j]
                else:
                    tab[i][j] = min(tab[i-1][j],A[current_node][j] + current_weight)
                
                
        current_node = indexMin(tab[i])
        if (current_node == -1):
            break
        current_weight = tab[i][current_node]
        best[current_node] = current_weight
        tab[i][current_node] = -2
        if current_node == N-1:
            break
        
    #print("best = {}\n tab = {}\n".format(best,tab))
    return best[N-1] + tasks[0]


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
