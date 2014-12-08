from arff import ArffReader
from collections import defaultdict
import itertools

# a set of arrays of tuples(attribute, value) is used as the data structure
# in order to store all the data needed.

# checkSupport checks if the conditions sent in tups have enough support
# (1.3.3) implementation
def checkSupport(tups, dataSet, minSupportCount):
    count = 0
    #first get a line from the dataset
    for buying, maint, persons, safety, classTarget in dataSet:
        # now check if the all values are in the line
        truthVal = True
        for attr,value in tups:
            if attr == 'buying' and buying != value:
                truthVal = False
            elif attr == 'maint' and maint != value:
                truthVal = False
            elif attr == 'persons' and persons != value:
                truthVal = False
            elif attr == 'safety' and safety != value:
                truthVal = False
            elif attr == 'class' and classTarget != value:
                truthVal = False

        if truthVal == True:
            count = count + 1
    return count >= minSupportCount



# this function implements the (1.3.1) "join" condition. it checks that the
# first k-1 elements are identical and that the last ones don't have the
# same attribute with a different value, but a completely different attribute
def isOneDifferent(cands1, cands2, level):
    # check for first k-1
    isTrue = True
    for i in range(level-1):
        if cands1[i] != cands2[i]:
            isTrue = False

    # check that kth is from different attribute
    attr1, val1 = cands1[level - 1]
    attr2, val2 = cands2[level - 1]
    if attr1 == attr2:
        isTrue = False;
    return isTrue

def mergeTups(cands1, cands2, level):
    tups = []
    #first k-1 are the same
    for i in range(level-1):
        tups.append(cands1[i])
    # only the last is different so add both
    tups.append(cands1[level-1])
    tups.append(cands2[level-1])
    return tups

# (1.3.2) this solves the subset condition by going to the combinations and making
# sure there are no smaller subsets included that don't already have support
def isValidNewTuple(tups, level, candidates, notSupported, dataSet):
    # check if any subset is among not supported ones
    for i in range(level):
        combos = itertools.combinations(tups, i)
        for e in combos:
            if e in notSupported:
                return False

    # got here means all subsets are valid
    # add to not supported if the count is not good enough
    if checkSupport(tups, dataSet, 3):
        return True
    else:
        notSupported.append(tups)
        return False


# creates the next level based on the previous ones
def createNextLevel(candidates, notSupported, level, dataSet):
    prevCandidates = candidates[level-1]
    for i in range(len(prevCandidates)):
        for j in range(i+1, len(prevCandidates)):
            if(isOneDifferent(prevCandidates[i],
                              prevCandidates[j], level-1)):
                newTuples = mergeTups(prevCandidates[i],
                                     prevCandidates[j],
                                     level-1)
                if(isValidNewTuple(newTuples, level, candidates,
                                 notSupported, dataSet)):
                    candidates[level].append(newTuples)


# function with the main intelligence
def apriori(inData, minSupportCount):
    # first create the set from initial data
    attributes = inData.attributes
    dataSet = inData.instances
    candidatesSet = {}
    notSupported = []
    k = 1
    candidatesSet[k] = []
    for attr in attributes:
        for val in attributes[attr]:
            tups = []
            tup = attr, val
            tups.append(tup)
            if checkSupport(tups, dataSet, minSupportCount):
                candidatesSet[k].append(tups)
            else:
                notSupported.append(tups)
    # now combine them and create higher order
    # stop condition: when there are no more rules to create
    while candidatesSet[k] != []:
        k += 1
        candidatesSet[k] = []
        createNextLevel(candidatesSet, notSupported, k, dataSet)

    print('------------')
    print('valid subsets ')
    print(candidatesSet)
    print('not supported')
    print(notSupported)


if __name__ == '__main__':
    # Example
    inData = ArffReader(open('data.arff'), keep_target=True)
    minSupportCount = 3
    apriori(inData, minSupportCount)
