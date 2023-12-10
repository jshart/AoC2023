from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day10/data/input_test.txt', 'r')
lines = file1.readlines()

# Here are the types of pipe connections
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

def connectsTo(c):
    retval=""

    #print("C2:"+c,end=" ")
    if c=="|":
        retval = "NS"
    elif c=="-":
        retval = "EW"
    elif c=="L":
        retval = "NE"
    elif c=="J":
        retval = "NW"
    elif c=="F":
        retval = "SE"
    elif c=="7":
        retval = "SW"
    elif c=="S":
        retval = "NESW"
    
    #print("Ret:"+retval)

    return retval

def connectForward(c,direction):
    validConnection=False

    if c=="|":
        if direction=="N" or direction=="S":
            validConnection=True
    elif c=="-":
        if direction=="E" or direction=="W":
            validConnection=True
    elif c=="L":
        if direction=="N" or direction=="E":
            validConnection=True
    elif c=="J":
        if direction=="N" or direction=="W":
            validConnection=True
    elif c=="F":
        if direction=="S" or direction=="E":
            validConnection=True
    elif c=="7":
        if direction=="S" or direction=="W":
            validConnection=True
    elif c=="S":
        validConnection=True
    
    return validConnection

def connectBackward(c,direction):
    validConnection=False

    if c=="|":
        if direction=="N" or direction=="S":
            validConnection=True
    elif c=="-":
        if direction=="E" or direction=="W":
            validConnection=True
    elif c=="L":
        if direction=="N" or direction=="E":
            validConnection=True
    elif c=="J":
        if direction=="N" or direction=="W":
            validConnection=True
    elif c=="F":
        if direction=="S" or direction=="E":
            validConnection=True
    elif c=="7":
        if direction=="S" or direction=="W":
            validConnection=True
    elif c=="S":
        validConnection=True
    
    return validConnection


def printMap(lines,msg):
    print("**** "+msg)
    for l in lines:
        temp="".join(l)
        temp2=temp.replace("."," ")
        print(temp2)

map=[]
# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMap=list(lines[c])
    map.append(tempMap)

printMap(map,"START STATE")

maxLoops=100
done=False
while not done and maxLoops>0:
    done=True
    maxLoops-=1

    for y,l in enumerate(map):
        for x,c in enumerate(l):
            # whats our boundary for this (UNUSED atm, but keeping here in case these are useful)
            checkXStart = x-1 if x>0 else x
            checkXEnd = x+1 if x<len(l)-1 else x
            checkYStart = y-1 if y>0 else y
            checkYEnd = y+1 if y<len(lines)-1 else y


            # which cells do we need to check for a valid
            # pipe connection based on this type?
            # This returns *All* of the connectinons that
            # need to met
            allowedDirections=connectsTo(c)

            # Build a matrix for what directions are valid and correct
            matrix={}
            for d in allowedDirections:
                matrix[d]=False

            #print(c,end=" ")
            #print(matrix, end=" -> ")

            # Based on the possible directions, lets check *EACH* if both sides of the
            # pipe see this as a legit connection
            if "N" in allowedDirections and y>0:
                if connectForward(map[y][x],"N") and connectBackward(map[y-1][x],"S"):
                    matrix["N"]=True
            if "S" in allowedDirections and y<len(lines)-1:
                if connectForward(map[y][x],"S") and connectBackward(map[y+1][x],"N"):
                    matrix["S"]=True
            if "E" in allowedDirections and x<len(l)-1:
                if connectForward(map[y][x],"E") and connectBackward(map[y][x+1],"W"):
                    matrix["E"]=True
            if "W" in allowedDirections and x>0:
                if connectForward(map[y][x],"W") and connectBackward(map[y][x-1],"E"):
                    matrix["W"]=True

            #print(matrix)

            goodConnection=True
            for m in matrix:
                if matrix[m]==False:
                    goodConnection=False
                    break

            # If this is a bad connetion and its not already a blank space, lets
            # reset it. We also treat S as an always valid space.
            if map[y][x]!="." and map[y][x]!="S":
                if not goodConnection:
                    #print("Replacing at:"+str(x)+","+str(y)+" with .")
                    map[y][x]="."
                    done=False

    printMap(map,"END STATE")