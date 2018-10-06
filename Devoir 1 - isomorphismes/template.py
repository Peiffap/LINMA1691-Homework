"""
    Students template for the first homework of LINMA1691 "Théorie des graphes".

    Authors : Philippe Matthew, Devillez Henri
"""

import itertools
import csv
from timeit import default_timer as timer


def check_mapping(A, B, h):
    """
    Input :
        - A, B two adjacency matrices (arrays of arrays) with same dimensions
        - h an array describing an isomorphism mapping node i from A to node h[i] from B  
    Return True if h(A) = B, False otherwise
    """

    n = len(A)
    for x in range(0, n):
            for y in range(x, n):
                if A[x][y] != B[h[x]][h[y]]:
                    return False

    return True


def are_iso(A, B):
    """
    Input :
        - A, B two adjacency matrices (arrays of arrays) with same dimensions
        
    Return (Ans, h) with :
        - Ans = True if A and B are isomorphic, False otherwise
        - h an array describing an isomorphism such that h(A) = B
    """

    n = len(A)

    nlist = []
    for x in range(0, n):
        nlist.append(x)

    perms = list(itertools.permutations(nlist))

    for x in range(0, len(perms)):
        if check_mapping(A, B, perms[x]):
            return True, perms[x]

    return False, []


def color_ones(A):
    """
    Input :
        - A an adjacency matrix (array of arrays)
        
    Return an array of same dimension as A containing only ones
    """

    color = []
    for x in range(0, len(A)):
        color.append(1)

    return color


def color_degree(A):
    """
    Input :
        - A an adjacency matrix (array of arrays)
    
    Return an array containing the degrees of the nodes of A
    """

    color = []
    for x in range(0, len(A)):
        color.append(sum(A[x]))

    return color


def color_k_neigh(A, k):
    """
    Input :
        - A an adjacency matrix (array of arrays)
        - k the size of the neighbourhood of the coloring scheme 
    
    Return an array containing the colors as defined in Q4 of the project statement
    The colors have to be structured as a sorted tuple of pairs (k, deg(v)) 
    """

    n = len(A)

    tuplist = []
    for x in range(0, n):
        tuplist.append([])

    Ak = A

    if k == 0:
        for i in range(0, n):
            tuplist.append((0, sum(A[i])))
        return tuplist

    if k == 1:
        for i in range(0, n):
            for j in range(0, n):
                if A[i][j] != 0:
                    tuplist[i].append((1, sum(A[j])))
        return tuplist

    klist = A
    for x in range(0, n):
        klist[x][x] = 1

    for x in range(1, k):
        for i in range(len(Ak)):
            for j in range(len(A[0])):
                for k in range(len(A)):
                    Ak[i][j] += Ak[i][k] * A[k][j]
        if x != k:
            for i in range(0, n):
                for j in range(i, n):
                    if Ak[i][j] != 0:
                        klist[i][j] = 1

    for i in range(0, n):
        for j in range(i, n):
            if klist[i][j] == 0 and Ak[i][j] != 0:
                tuplist[i].append((k, sum(A[j])))
        sorted(tuplist[i], key=lambda tup: tup[1])

    return tuplist
     

def are_iso_with_colors(A, B, color=color_ones):
    """
    Input :
        - A, B two adjacency matrices (arrays of arrays) with same dimensions
        - color a coloring function
    Return (Ans, h) using the coloring heuristic with :
        - Ans = True if A and B are isomorphic, False otherwise
        - h describes an isomorphism such that h(A) = B if Ans = True, h = [] otherwise
    
    """

    n = len(A)

    colora = color(A)
    colorb = color(B)

    h = []
    aused = []
    bused = []
    bskips = []

    for x in range(n):
        h.append(0)
        aused.append(0)
        bused.append(0)
        bskips.append([])
        for y in range(n):
            bskips[x].append(0)

    def same_edges(A, B, h, i):
        for x in range(0, n):
            if aused[x] == 1 and A[i][x] != B[h[i]][h[x]]:
                return False
        return True

    def clean_mat(M, i):
        for j in range(n):
            M[i][j] = 0

    def tried_all(colora, colorb, skips):
        for x in range(n):
            if skips[0][x] == 0 and colora[0] == colorb[x]:
                return False
        return True

    def isom_color(A, B, h, i):
        if not same_edges(A, B, h, i):
            return False, h
        flag = 0
        for x in range(n):
            if aused[x] == 0:
                flag = 1
                break
        if flag == 0:
            return True, h
        nodeA = 0
        while nodeA < n:
            if aused[nodeA] == 0:
                nodeB = 0
                while nodeB < n:
                    if bused[nodeB] == 0 and bskips[nodeA][nodeB] == 0 and colora[nodeA] == colorb[nodeB]:
                        h[nodeA] = nodeB
                        aused[nodeA] = 1
                        bused[nodeB] = 1
                        truth, h = isom_color(A, B, h, nodeA)
                        if truth:
                            return True, h
                        elif h:
                            aused[nodeA] = 0
                            bused[nodeB] = 0
                        else:
                            return False, []
                    nodeB += 1
                clean_mat(bskips, nodeA)
                nodeA -= 1
                bskips[nodeA][h[nodeA]] = 1
                bused[h[nodeA]] = 0
                aused[nodeA] = 0
                nodeA -= 1  # bc +1 is gonna happen below
                if nodeA < 0 and tried_all(colora, colorb, bskips):
                    return False, []
            nodeA += 1
        return False, []

    return isom_color(A, B, h, 0)


if __name__ == "__main__":

    start = timer()

    # Read Input
    
    with open('in1.csv', 'r') as fd:
        lines = list(csv.reader(fd, delimiter=','))
        n = int(len(lines)/2)

        A = []
        B = []

        for i in range(n):
            A.append([int(x) for x in lines[i]])
        
        for j in range(n, 2*n):
            B.append([int(x) for x in lines[j]])  
            
    # Compute answer

    #for i in range(0, 1000):
    #    are_iso, h = are_iso_with_colors(A, B, color_ones)
    #are_iso, h = are_iso(A, B)
    are_iso, h = are_iso_with_colors(A, B, color_degree)
    # are_iso, h = are_iso_with_colors(A, B, lambda x: color_k_neigh(x, 2))
     
    # Check results

    with open('out1.csv', 'r') as fd:
        lines = csv.reader(fd, delimiter=',')
        true_answer = int(next(lines)[0])
        
        if are_iso != true_answer:
            if true_answer:
                print("Wrong answer: A and B are isomorphic")
            else:
                print("Wrong answer: A and B are not isomorphic")
        else:
            if are_iso:
                if check_mapping(A, B, h):
                    print("Correct answer")
                else:
                    print("Wrong answer: incorrect mapping")

    end = timer()
    print(end - start)
