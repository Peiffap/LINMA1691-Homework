"""
    Student template for the third homework of LINMA1691 "Théorie des graphes".

    Authors : Devillez Henri
"""

import math
    
def spanning_tree_1(N, roads):
    """ 
    INPUT : 
        - N, the number of crossroads
        - roads, list of tuple (u, v, s) giving a road between u and v with satisfaction s
    OUTPUT :
        - return the maximal satisfaction that can be achieved
        
        See homework statement for more details
    """
    
    # We construct a "arbre sous tendant de poids min" and we sum the weight
    # of the roads left out of this tree
    
    # Pas sur que c'est bon
    # Sorting roads by weight
    roads = sorted(roads,key=lambda tup: tup[2])
    M = len(roads)
    
    # S saves the nodes already in the tree
    # S[i] = 0 if the node is not in yet
    # S[i] = 1 if the node is already in
    S = [0]*N

    # n = nonzero element of S
    n = 0
    
    # i is the index of the current road
    # M is the current number of arete left
    i = 0
    while(i < M):
        #print("M = {}, i = {}, n = {}, roads = {}".format(M,i,n,roads))
        u = roads[i][0]
        v = roads[i][1]
        
        # if u and v are in S (->S[u]=S[v]=1 then the arete i will form a cycle
        if (S[u] == 0 or S[v] == 0):
            
            # if S[u] = S[v] = 0
            if(S[u] == S[v]):
                n += 2
            else:
                n += 1
            S[u] = 1
            S[v] = 1
            del roads[i]
            M = M - 1
            if (n == N):
                break
        else:
            i += 1

    # Satisfaction is the sum of the roads left
    return sum([road[2] for road in roads])

    
if __name__ == "__main__":

    # Read Input for the first exercice
    
    with open('in1.txt', 'r') as fd:
        l = fd.readline()
        l = l.rstrip().split(' ')
        
        n, m = int(l[0]), int(l[1])
        
        roads = []
        for road in range(m):
        
            l = fd.readline().rstrip().split()
            roads.append(tuple([int(x) for x in l]))
            
    # Compute answer for the first exercice
     
    ans1 = spanning_tree_1(n, roads)
     
    # Check results for the first exercice

    with open('out1.txt', 'r') as fd:
        l_output = fd.readline()
        expected_output = int(l_output)
        
        if expected_output == ans1:
            print("Exercice 1 : Correct")
        else:
            print("Exercice 1 : Wrong answer")
            print("Your output : %d ; Correct answer : %d" % (ans1, expected_output)) 
        

