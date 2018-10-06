"""
    Students template for the first homework of LINMA1691 "Th√©orie des graphes".

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

    # TO COMPLETE
    
    n = len(A) #Longueur de A
    
    #Matrice nulle
    AkNext = []
    for x in range(0, n):
        AkNext.append([])
        for y in range(0, n):
            AkNext[x].append(0)
    #List a renvoyer
    tuplist = []
    for x in range(0, n):
        tuplist.append([])
    
    #Copier ELEMENT PAR ELEMENT A dans Ak
    Ak = []
    for x in range(0, n):
        Ak.append([])
        for y in range(0, n):
            Ak[x].append(A[x][y])
    
    #Garde en memoire les chemins deja comptes: 1 = pas encore compte, 0 = counted       
    klist = []
    for x in range(0, n):
        klist.append([])
        for y in range(0, n):
            klist[x].append(1)
   

    #d itere toutes les valeurs de k, de 0 a k compris
    for d in range(0,k+1):
        
        #Cas singulier k == 0 : tout les noeuds sont a une distance 0 de eux meme
        if d == 0:
            for i in range(0, n):
                tuplist[i].append((0, sum(A[i])))
                klist[i][i] = 0

            
        #Cas singulier k == 1 : on utilise la matrice A^1
        elif d == 1:
            for i in range(0, n):
                for j in range(0, n):
                    if klist[i][j] == 1 and A[i][j] != 0:
                        tuplist[i].append((1, sum(A[j])))
                        tuplist[i] = sorted(tuplist[i])
                        klist[i][j] = 0
                        
        #Cas quelconque
        else:

            #Calcul de A^k
            for i in range(0, n):
                for j in range(0, n):
                       for m in range(0, n):
                           #Matrice nulle = Ak * A
                           AkNext[i][j] += Ak[i][m] * A[m][j]

            for x in range(0, n):
                for y in range(0, n):
                    #Copier ELEMENT PAR ELEMENT AkNext (=Ak+1) dans Ak et mettre AkNext ‡ 0
                    Ak[x][y] = AkNext[x][y]
                    AkNext[x][y] = 0
            
            #Construction de tuplist
            for i in range(0, n):
                for j in range(0, n):
                    if klist[i][j] == 1 and A[i][j] != 0:
                        tuplist[i].append((d, sum(A[j])))
                        tuplist[i] = sorted(tuplist[i])
                        klist[i][j] = 0


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

    colorA = color(A)
    colorB = color(B)

    Aused = []
    Bused = []
    for x in range(0, n):
        Aused.append(n+1)
        Bused.append(n+1)

    def same_edges(A, B, h, i):
        for x in range(0, n):
            if h[x] != n+1 and A[i][x] != B[h[i]][h[x]]:
                return False
        return True

    def isom_color(A, B, h, hinv, i):
        if i != n+1 and not same_edges(A, B, h, i):
            return False, h
        flag = 0
        for x in range(0, n):
            if h[x] == n+1:
                flag = 1
                break
        if flag == 0:
            return True, h
        for nodeA in range(0, n):
            if h[nodeA] == n+1:
                for nodeB in range(0, n):
                    if hinv[nodeB] == n+1 and colorA[nodeA] == colorB[nodeB]:
                        print(nodeA)
                        print(nodeB)
                        h[nodeA] = nodeB
                        hinv[nodeB] = nodeA
                        boole, h = isom_color(A, B, h, hinv, nodeA)
                        if boole:
                            return True, h
                        elif h:
                            h[nodeA] = n+1
                            hinv[nodeB] = n+1
                        else:
                            return False, []

                if h[nodeA] == n+1:
                    return False, []
        return False, []

    return isom_color(A, B, Aused, Bused, n+1)


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

    for i in range(0, 1000):
        are_iso, h = are_iso_with_colors(A, B, color_ones)
    #are_iso, h = are_iso(A, B)
    #for i in range(0, 1000):
    #    are_iso, h = are_iso_with_colors(A, B, color_degree)
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
