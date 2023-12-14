from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day14/data/input_test.txt', 'r')
lines = file1.readlines()

class Dish:
    def __int__(self,map):
        self.map=[]
        self.copyMap(map)

    def copyMap(self,m):
        for i in range(0,len(m)):
            self.map.append(m[i].copy())

    def printMap(self):
        for i in range(0,len(self.map)):
            for j in range(0,len(self.map[i])):
                print(self.map[i][j],end="")
            print()


map=[]


def tiltNorth(map):
    somethingMoved=True
    while somethingMoved:
        somethingMoved=False
        for i in range(1,len(map)):

            # print("processing:[",end="")
            # print(map[i],end="")
            # print("] index="+str(i))
            # lets check each character in the row
            # looking for a rock we can move
            for j in range(0,len(map[i])):
                if map[i][j]=="O":
                    # is the cell above empty?
                    if map[i-1][j]==".":
                        # move the rock up
                        map[i-1][j]="O"
                        map[i][j]="."
                        somethingMoved=True

def tiltSouth(map):
    somethingMoved=True
    while somethingMoved:
        somethingMoved=False
        for i in range(len(map)-2,-1,-1):

            # print("processing:[",end="")
            # print(map[i],end="")
            # print("] index="+str(i))
            # lets check each character in the row
            # looking for a rock we can move
            for j in range(0,len(map[i])):
                if map[i][j]=="O":
                    # is the cell above empty?
                    if map[i+1][j]==".":
                        # move the rock up
                        map[i+1][j]="O"
                        map[i][j]="."
                        somethingMoved=True

def tiltEast(map):
    somethingMoved=True
    while somethingMoved:
        somethingMoved=False
        for j in range(0,len(map[0])-1):
            # print("processing:[",end="")
            # print(map[j],end="")
            # print("] index="+str(j))
            # lets check each character in the row
            # looking for a rock we can move
            for i in range(0,len(map)):
                if map[i][j]=="O":
                    # is the cell above empty?
                    if map[i][j+1]==".":
                        # move the rock up
                        map[i][j+1]="O"
                        map[i][j]="."
                        somethingMoved=True

def tiltWest(map):
    somethingMoved=True
    while somethingMoved:
        somethingMoved=False
        for j in range(len(map[0])-1,0,-1):
            # print("processing:[",end="")
            # print(map[j],end="")
            # print("] index="+str(j))
            # lets check each character in the row
            # looking for a rock we can move
            for i in range(0,len(map)):
                if map[i][j]=="O":
                    # is the cell above empty?
                    if map[i][j-1]==".":
                        # move the rock up
                        map[i][j-1]="O"
                        map[i][j]="."
                        somethingMoved=True


def runCycle(map):
    # Tilt North
    tiltNorth(map)
    # Tilt West
    tiltWest(map)
    # Tilt South
    tiltSouth(map)
    # Tilt East
    tiltEast(map)

def compareMaps(o,n):
    for i in range(0,len(o)):
        for j in range(0,len(o[i])):
            if o[i][j]!=n[i][j]:
                return False
    return True

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMapLine=list(lines[c])
    map.append(tempMapLine)
    print(map[-1])

print("**** DATA LOAD COMPLETE, starting run")
print("**** INITIAL MAP - taking a copy ****")
originalMap=[]
for i in range(0,len(map)):
    originalMap.append(map[i].copy())

cycles=1000000000
#cycles=1
c=0

print("MAP compare check:"+str(compareMaps(map,map)))

while True:
    runCycle(map)
    c+=1
    same=compareMaps(originalMap,map)
    if same:
        print("**** REACHED SAME MAP **** After:"+str(c))
        break
    else:
        if c % 1000 == 0:
            print("**** MAP IS STILL DIFFERENT **** After:"+str(c))

    if c == cycles:
        break
    
print("**** FINAL MAP ****")
printMap(map)

totalScore=0
# Score the grid
for c,m in enumerate(map):
    # how many rocks are in this row?
    rocks=m.count("O")
    lineScore=rocks*(len(map)-c)
    print("Line "+str(c)+" has "+str(rocks)+" rocks, score="+str(lineScore))
    totalScore+=lineScore

# Print the final total score
print("Total Score = "+str(totalScore))

# Part 1 answer: 106378
# didnt cycle back to original map after; After:17953000 cycles