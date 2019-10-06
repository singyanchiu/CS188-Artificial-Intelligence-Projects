
import itertools

cornersRemaining = [(1,1), (5,1), (5,4)]

currentPosition = (4,3)

def manhattan(startPosition, targetPosition):
    xy1 = startPosition
    xy2 = targetPosition
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

if len(cornersRemaining) == 0:
    final = 0
if len(cornersRemaining) == 1:
    final = manhattan(currentPosition, cornersRemaining[0])
    print("min of all distances = ", final, "\n")
if len(cornersRemaining) > 1:
    #find all permutations of cornersRemaining meaning all possible way of traveling thru them
    totalDistances = []
    totalDistance = 0
    cornersRemainingAllPerm = list(itertools.permutations(cornersRemaining))
    #print("cornersRemainingAllPerm = ",cornersRemainingAllPerm)
    for perm in cornersRemainingAllPerm:
        print("Permutation = ", perm)
        totalDistance = manhattan(currentPosition, perm[0])
        for i in range(len(perm)-1):
            totalDistance += manhattan(perm[i], perm[i+1])
        print("Total Distance for this perm = ", totalDistance)
        totalDistances.append(totalDistance)

    final = min(totalDistances)
    #print("all distances = ", totalDistances)
    print("min of all distances = ", final, "\n")
