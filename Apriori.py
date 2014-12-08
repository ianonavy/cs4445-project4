from ArffReader import ArffReader
from collections import defaultdict
import itertools

# a set of arrays of tuples(attribute, value) is used as the data structure
# in order to store all the data needed.

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
     
                    

def isOneDifferent(cands1, cands2, level):
    isTrue = True
    for i in range(level-1):
        if cands1[i] != cands2[i]:
            isTrue = False

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

def isValidNewTuple(tups, level, candidates, notSupported, dataSet):
    # check if any subset is among not supported ones
    for i in range(level):
        combos = itertools.combinations(tups, i)
        for e in combos:
            if e in notSupported:
                return False

    # got here means all subsets are valid
    if checkSupport(tups, dataSet, 3): # TODO 3 from minSupportCount
        return True
    else:
        notSupported.append(tups)
        return False
    
    

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
                

def apriori(inData, minSupportCount):
    # first create the set from initial data
    attributes = inData.attributes
    dataSet = inData.to_list_of_lists()
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
    inData = ArffReader(open('data.arff'))
    minSupportCount = 3
    apriori(inData, minSupportCount)
