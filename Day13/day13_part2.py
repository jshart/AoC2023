from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day13/data/input.txt', 'r')
lines = file1.readlines()

map=[]


# TODO - see if these 2 functions, function as designed :D
# def compareRows(map,u,d):
#     for k in range(len(map[u])):
#         if map[u] != map[d]:
#             return False
#     return True

# def compareCols(map,l,r):
#     for row in range(len(map)):
#         if map[row][l] != map[row][r]:
#             return False
            
#     return True

def checkRepeatedRow(map):
    for i in range(len(map)-1):

        wildCardUsed=False
        matched=True
        for k in range(len(map[i])):
            if map[i][k] != map[i+1][k]:
                if wildCardUsed==False:
                    wildCardUsed=True
                    print("ROW Looking for initial match - using wildcard on (row/col):"+str(i)+","+str(k))
                else:
                    matched=False

        if matched:
            print("ROW Found a potential mirror at row:"+str(i)+"="+str(i+1))
            u=i-1
            d=i+2
            mirrored=True
            while u>=0 and d<len(map):
                print("ROW Checking rows:"+str(u)+","+str(d))

                rowsMatch=True
                # Loop through each char in the row
                for k in range(len(map[0])):
                    if map[u][k] != map[d][k]:
                        if wildCardUsed==False:
                            wildCardUsed=True
                            print("ROW using wildcard for follow on:"+str(u)+","+str(k))
                        else:                        
                            rowsMatch=False
                            break

                if rowsMatch==False:
                    print("ROW Found mirror DISPROVED")
                    mirrored=False
                    break
                u-=1
                d+=1


            if mirrored and wildCardUsed:
                print("ROW Found mirror CONFIRMED")
                score = i+1
                printRow(map, i)
                return score

    return -1

def checkRepeatedCol(map):
    # loop through each column checking each item in that column
    # with the one next to it
    # Start with a loop that visits each column
    for col in range(len(map[0])-1):

        wildCardUsed=False
        matched=True
        # loop through each row checking each item in that column
        for row in range(len(map)):
            if map[row][col] != map[row][col+1]:
                if wildCardUsed==False:
                    wildCardUsed=True
                    print("COL looking for initial match - using wildcard on:"+str(col)+","+str(row))
                else:
                    matched=False

        if matched:
            print("COL Found a potential mirror at col:"+str(col)+"="+str(col+1))
            l=col-1
            r=col+2
            mirrored=True
            while l>=0 and r<len(map[0]):
                print("COL Checking cols:"+str(l)+","+str(r))

                colsMatch=True
                for row in range(len(map)):
                    if map[row][l] != map[row][r]:
                        if wildCardUsed==False:
                            wildCardUsed=True
                            print("COL using wildcard for follow on col:"+str(l)+","+str(row))
                        else:                        
                            colsMatch=False
                            break

                if colsMatch==False:
                    print("COL Found mirror DISPROVED")
                    mirrored=False
                    break
                l-=1
                r+=1 

            if mirrored and wildCardUsed:
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

def checkForMirror(map):
    print("*** Checking Col")
    cRet = checkRepeatedCol(map)

    print("*** Checking Row")
    rRet = checkRepeatedRow(map)

    if cRet>0 and rRet>0:
        if cRet<rRet:
            return cRet
        else:
            return rRet*100
    elif cRet>0:
        return cRet
    elif rRet>0:
        return rRet*100
    
  

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


# too low: 20127,24561