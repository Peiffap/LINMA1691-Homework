"""
    Solution for the fourth homework of LINMA1691 "Théorie des graphes".

    Authors : Devillez Henri
"""

import math


def matching(T, friends, hiding_places):
    """ 
    INPUT : 
        - T, the number of seconds
        - friends, a list of tuples (x, y, v) describing the position (x, y) and velocity v
          of each friend
        - hiding_places, a list of tuple (x, y) giving the position (x, y) of each hiding place
    OUTPUT :
        - return the maximal number of friends that can hide from the game master
        
        See homework statement for more details
    """
    
    ans = 0

    adj_mat = []
    for i in range(len(friends)):
        adj_mat.append([])
        for j in range(len(hiding_places)):
            distx = hiding_places[j][0] - friends[i][0]
            disty = hiding_places[j][1] - friends[i][1]
            time = math.sqrt(distx*distx + disty*disty)/friends[i][2]
            adj_mat[i].append(time)

    matching = []
    while len(matching) < min(len(friends), len(hiding_places)):

        a = 1

    return ans

    
if __name__ == "__main__":

    # Read Input
    
    with open('in1.txt', 'r') as fd:
        l = fd.readline()
        l = l.rstrip().split(' ')
        
        m, n, T = int(l[0]), int(l[1]), int(l[2])  # fixed maybe?

        friends = []
        for friend in range(n):
            l = fd.readline().rstrip().split()
            friends.append(tuple([float(x) for x in l]))
       
        hiding_places = []
        for hiding_place in range(m):
            l = fd.readline().rstrip().split()
            hiding_places.append(tuple([float(x) for x in l]))

    # Compute answer 
     
    ans = matching(T, friends, hiding_places)
     
    # Check results 

    with open('out1.txt', 'r') as fd:
        l_output = fd.readline()
        expected_output = int(l_output)
        
        if expected_output == ans:
            print("Test sample : Correct")
        else:
            print("Test sample : Wrong answer")
            print("Your output : %d ; Correct answer : %d" % (ans, expected_output))