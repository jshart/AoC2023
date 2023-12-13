from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day13/data/input.txt', 'r')
lines = file1.readlines()

map=[]


# TODO - see if these 2 functions, function as designed :D
def compareRows(map,i,j):
    if map[i] == map[j]:
        return True
    return False

def compareCols(map,i,j):
    for row in range(len(map)):
        if map[row][i] != map[row][j]:
            return False
            
    return True

def checkRepeatedRow(map):
    for i in range(len(map)-1):
        if map[i] == map[i+1]:
            print("ROW Found a potential mirror at row:"+str(i)+"="+str(i+1))
            u=i-1
            d=i+2
            mirrored=True
            while u>=0 and d<len(map)-1:
                #print("ROW Checking rows:"+str(u)+","+str(d))

                if compareRows(map,u,d)==False:
                    print("ROW Found mirror DISPROVED")

                    mirrored=False
                    break
                u-=1
                d+=1


            if mirrored:
                print("ROW Found mirror CONFIRMED")
                score = (i+1)*100
                printRow(map, i)
                return score

    return -1

def checkRepeatedCol(map):
    # loop through each column checking each item in that column
    # with the one next to it
    # Start with a loop that visits each column
    for col in range(len(map[0])-1):

        matched=True
        # loop through each row checking each item in that column
        for row in range(len(map)):
            if map[row][col] != map[row][col+1]:
                matched=False

        if matched:
            print("COL Found a potential mirror at col:"+str(col)+"="+str(col+1))
            l=col-1
            r=col+2
            mirrored=True
            while l>=0 and r<len(map[0]):
                #print("COL Checking cols:"+str(l)+","+str(r))

                if compareCols(map,l,r)==False:
                    print("COL Found mirror DISPROVED")

                    mirrored=False
                    break
                l-=1
                r+=1 

            if mirrored:
                print("COL Found mirror CONFIRMED")
                score = col+1
                printCol(map, col)
                return score

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
    print("*** Checking Col")
    ret = checkRepeatedCol(map)
    if ret<0:
        print("*** Checking Row")
        ret = checkRepeatedRow(map)
    return ret

mirrorCount=0
fCount=0
totalScore=0
print("-------01234567890123456789")

while True:
    line = lines.pop(0)
    line=line.strip()

    if len(line)<1:
        mirrorCount+=1
        print("*** Mirror:"+str(mirrorCount))
        print(map)
        score=checkForMirror(map)
        print("Score: "+str(score))
        print("**** MIRROR COMPLETE, reloading for next")
        print("-------01234567890123456789")

        totalScore+=score
        map.clear()
        fCount=0
    else:
        print("Fetch:{"+line+"} "+str(fCount))
        fCount+=1
        map.append(line.strip())

    if len(lines) == 0:
        break


print("Final Score: "+str(totalScore))


# too low; 26370
# too low; 30000
# too high; 33246