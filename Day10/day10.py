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
    retval = "NS" if c=="|" else ""
    retval = "EW" if c=="-" else ""
    retval = "NE" if c=="L" else ""
    retval = "NW" if c=="J" else ""
    retval = "SE" if c=="F" else ""
    retval = "SW" if c=="7" else ""
    
    return retval

def inversionConnection(c):
    retval = "NS" if c=="|" else ""
    retval = "EW" if c=="-" else ""
    retval = "SW" if c=="L" else ""
    retval = "SE" if c=="J" else ""
    retval = "NW" if c=="F" else ""
    retval = "NE" if c=="7" else ""
    
    return retval


def printMap(lines,msg):
    print("**** "+msg)
    for l in lines:
        print(l)

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()

printMap(lines,"START STATE")

for y,l in enumerate(lines):
    for x,c in enumerate(l):
        # check the cells around this
        iCanConnectUsing=connectsTo(c)
        
        checkXStart = x-1 if x>0 else x
        checkXEnd = x+1 if x<len(l)-1 else x
        checkYStart = y-1 if y>0 else y
        checkYEnd = y+1 if y<len(lines)-1 else y

        for checkX in range(checkXStart,checkXEnd+1):
            for checkY in range(checkYStart,checkYEnd+1):
                if checkX==x and checkY==y:
                    continue

                allowedToConnectUsing=inversionConnection(lines[checkY][checkX])
                
                # check each permitted direction to see if there is a match
                goodConnection=False
                for a in allowedToConnectUsing:
                    print("testing:"+a,end="")
                    if a in iCanConnectUsing:
                        goodConnection=True
                        print(" YES")
                    else:
                        print(" NO")

                if not goodConnection:
                    lines[y]=lines[y].replace(c,".")

printMap(lines,"END STATE")