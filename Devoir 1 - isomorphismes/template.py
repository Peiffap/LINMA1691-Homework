"""
    Students template for the first homework of LINMA1691 "Théorie des graphes".

    Authors : Philippe Matthew, Devillez Henri
"""

import itertools
import csv


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
        color.append([])
        for y in range(0, len(A)):
            color[x].append(1)

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

    # TO COMPLETE
            
    return []
     

def are_iso_with_colors(A, B, color=color_ones):
    """
    Input :
        - A, B two adjacency matrices (arrays of arrays) with same dimensions
        - color a coloring function
    Return (Ans, h) using the coloring heuristic with :
        - Ans = True if A and B are isomorphic, False otherwise
        - h describe an isomorphism such that h(A) = B if Ans = True, h = [] otherwise
    
    """

    n = len(A)

    nlist = []
    for x in range(0, n):
        nlist.append(x)

    perms = list(itertools.permutations(nlist))

    colorA = color_degree(A)
    colorB = color_degree(B)

    for x in range(0, len(perms)):
        permsx = perms[x]
        for y in range(0, n):
            if colorA[y] != colorB[permsx[y]]:
                break

        if check_mapping(A, B, permsx):
            return True, permsx

    return False, []


if __name__ == "__main__":

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
     
    # are_iso, h = are_iso_with_colors(A, B, color_ones)
    are_iso, h = are_iso_with_colors(A, B, color_degree)
    # are_iso, h = are_iso_with_colors(A, B, lambda x : color_k_neigh(x, 2))
     
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
                
            

        
