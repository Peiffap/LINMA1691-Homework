"""
    Students template for the second homework of LINMA1691 "Théorie des graphes".

    Authors : Devillez Henri
"""


import queue as Q
from collections import deque
import random
from timeit import default_timer as timer

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

    wall, clear, endchar, startchar = '#', '.', 'S', 'E'
    height = len(maze)
    width = len(maze[0])

    def find_start(grid):
        for y in range(1, height-1):
            for x in range(1, width-1):
                if grid[y][x] == startchar:
                    return (x, y, 0)

    start = find_start(maze)

    queue = deque([start])

    seen = {start}
    while queue:
        x, y, d = queue.popleft()

        if not 0 < x < width:
            continue

        if not 0 < y < height:
            continue

        if maze[y][x] == wall:
            continue

        if maze[y][x] == endchar:
            return d

        if (x, y) in seen:
            continue

        seen.add((x, y))

        for (x2, y2) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            queue.append((x2, y2, d+1))

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
    
    # "Adjacence matrix"
    A = []   
    
    # List of the best ways
    best = []
    
    tab  = []

    # Initialiazing of A, tab and best
    for i in range(0, N):        
        A.append([])
        tab.append([])
        best.append(0)
        for j in range(0, N):                           
                A[i].append(-1)
                tab[i].append(0)
                
    # Computation oh the weight of each arete            
    for i in range(0, len(paths)):        
        A[paths[i][0]-1][paths[i][1]-1] = paths[i][2] + tasks[paths[i][1]-1]
        A[paths[i][1]-1][paths[i][0]-1] = paths[i][2] + tasks[paths[i][0]-1]

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

            if tab[i-1][j] == -2: # Already in best
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
                    tab[i][j] = min(tab[i-1][j], A[current_node][j] + current_weight)
                                
        current_node = indexMin(tab[i])
        if (current_node == -1):
            break
        current_weight = tab[i][current_node]
        best[current_node] = current_weight
        tab[i][current_node] = -2
        if current_node == N-1:
            break
        
    return best[N-1] + tasks[0]


def MazeGenerator(xSize =1000, ySize =1000):
    """
        Generateur de Labyrinthe pour le cours LINMA1691
        Input : Taille du labyrinthe (X > 4, Y >4)
        Output : Labyrinthe (à priori) résolvable
        Author : Florian Damhaut
        SourceCode labyrinthe : FB36
    """
    mx = xSize-2
    my = ySize-2
    if mx < 2 or my < 2:
        return -1
    maze = [[0 for x in range(mx)] for y in range(my)]
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]  # 4 directions to move in the maze
    # start the maze from a random cell
    stack = [(random.randint(0, mx - 1), random.randint(0, my - 1))]

    while len(stack) > 0:
        (cx, cy) = stack[-1]
        maze[cy][cx] = 1
        # find a new cell to add
        nlst = []  # list of available neighbors
        for i in range(4):
            nx = cx + dx[i]; ny = cy + dy[i]
            if 0 <= nx < mx and 0 <= ny < my:
                if maze[ny][nx] == 0:
                    # of occupied neighbors must be 1
                    ctr = 0
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if 0 <= ex < mx and 0 <= ey < my:
                            if maze[ey][ex] == 1:
                                ctr += 1
                    if ctr == 1: nlst.append(i)
        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]
            stack.append((cx, cy))
        else:
            stack.pop()

    # On remet aux normes du devoir
    revampmaze = [['#' for x in range(mx+2)] for y in range(my+2)]
    for irow, row in enumerate(maze):
        for icol, home in enumerate(row):
            if home == 1:
                revampmaze[irow+1][icol+1] = '.'

    # Entree/Sortie Aleatoire
    E = False
    while not E:
        pos = (random.randint(0, mx)+1, random.randint(0, my)+1)
        if revampmaze[pos[0]][pos[1]] == '.':
            revampmaze[pos[0]][pos[1]] = 'E'
            E = True

    S = False
    while not S:
        pos = (random.randint(0, mx)+1, random.randint(0, my)+1)
        if revampmaze[pos[0]][pos[1]] == '.':
            revampmaze[pos[0]][pos[1]] = 'S'
            S = True

    return revampmaze


if __name__ == "__main__":

    # Read Input for the first exercise

    with open('in3.txt', 'r') as fd:
        l = fd.readline()
        l = l.split(' ')

        n = int(l[0])
        m = int(l[1])

        maze = []
        for row in range(n):
            l = fd.readline().rstrip()
            maze.append(list(l))

    # Compute answer for the first exercise
    maze = MazeGenerator(1000, 1000)
    a = timer()
    ans1 = shortest_path_1(maze)

    b = timer()
    print(b-a)

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
