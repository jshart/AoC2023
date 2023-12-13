from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day13/data/input_test.txt', 'r')
lines = file1.readlines()

map=[]

def checkRepeatedRow(map):
    for i in range(len(map)):
        if map[i] == map[i+1]:
            return i
    return -1

def checkRepeatedCol(map):
    # loop through each column checking each item in that column
    # with the one next to it
    for i in range(len(map[0])):
        for j in range(len(map)):
            if map[j][i] == map[j+1][i]:
                return i
            
    return -1

def printRow(map, row):
    for i in range(len(map[row])):
        print(map[row][i], end='')
    print()

def printCol(map, col):
    for i in range(len(map)):
        print(map[i][col], end='')
    print()

# TODO - need to come back in here and actually check the rest
# of the rows/cols actually are mirrored before declaring this
# a mirror, just looking at the single dup row/col otherwise
# turns up false postives.
def checkForMirror(map):
    ret = checkRepeatedRow(map)
    if ret != -1:
        score = len(map) - ret
        printRow(map, ret)
        return score
    
    ret = checkRepeatedCol(map)
    if ret != -1:
        score = (len(map[0]) - ret)*100
        printCol(map, ret)
        return score
    return -1

mirrorCount=0
while True:
    line = lines.pop(0)
    line=line.strip()

    print("Fetch: {"+line+"}")

    if len(line)<1:
        mirrorCount+=1
        print("*** Mirror:"+str(mirrorCount))
        print(map)
        score=checkForMirror(map)
        print("Score: "+str(score))
        map.clear()
    else:
        map.append(line.strip())

    if len(lines) == 0:
        break