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
    
    # Sorting roads by weight
    roads = sorted(roads,key=lambda tup: tup[2])
    # M_init is the initial number of road
    M_init = len(roads)
    
    # M is the current number of road left
    M = M_init
    
    # P is a partition of the graph
    P = [i for i in range(0,N)]
    
    # i is the index of the current road
    i = 0
    
    while(i < M):
        #print("M = {}, i = {}, P = {}, roads = {}".format(M,i,P,roads))
        u = roads[i][0]
        v = roads[i][1]
        
        # if u and v are not in the same partition then put them together
        if (P[u] != P[v]):
            # union the partitions
            Pv = P[v]
            for j in range(0,N):
                if P[j] == Pv:
                    P[j] = P[u]
            del roads[i] 
            M -= 1
                  
            # M_init - M is the number of aretes in the tree
            if (M_init - M == N - 1):
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
        

