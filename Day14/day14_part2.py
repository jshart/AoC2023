from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day14/data/input_test.txt', 'r')
lines = file1.readlines()

class Dish:
    def __init__(self,m):
        self.map=[]
        self.copyMap(m)

    def copyMap(self,m):
        for i in range(0,len(m)):
            self.map.append(m[i].copy())

    def printMap(self):
        for i in range(0,len(self.map)):
            for j in range(0,len(self.map[i])):
                print(self.map[i][j],end="")
            print()

    def tiltNorth(self):
        somethingMoved=True
        while somethingMoved:
            somethingMoved=False
            for i in range(1,len(self.map)):
                for j in range(0,len(self.map[i])):
                    if self.map[i][j]=="O":
                        # is the cell above empty?
                        if self.map[i-1][j]==".":
                            # move the rock up
                            self.map[i-1][j]="O"
                            self.map[i][j]="."
                            somethingMoved=True

    def tiltSouth(self):
        somethingMoved=True
        while somethingMoved:
            somethingMoved=False
            for i in range(len(self.map)-2,-1,-1):
                for j in range(0,len(self.map[i])):
                    if self.map[i][j]=="O":
                        # is the cell above empty?
                        if self.map[i+1][j]==".":
                            # move the rock up
                            self.map[i+1][j]="O"
                            self.map[i][j]="."
                            somethingMoved=True

    def tiltEast(self):
        somethingMoved=True
        while somethingMoved:
            somethingMoved=False
            for j in range(0,len(self.map[0])-1):
                for i in range(0,len(self.map)):
                    if self.map[i][j]=="O":
                        # is the cell above empty?
                        if self.map[i][j+1]==".":
                            # move the rock up
                            self.map[i][j+1]="O"
                            self.map[i][j]="."
                            somethingMoved=True

    def tiltWest(self):
        somethingMoved=True
        while somethingMoved:
            somethingMoved=False
            for j in range(len(self.map[0])-1,0,-1):
                for i in range(0,len(self.map)):
                    if self.map[i][j]=="O":
                        # is the cell above empty?
                        if self.map[i][j-1]==".":
                            # move the rock up
                            self.map[i][j-1]="O"
                            self.map[i][j]="."
                            somethingMoved=True

    def compareMaps(self,n):
        for i in range(0,len(self.map)):
            for j in range(0,len(self.map[i])):
                if self.map[i][j]!=n[i][j]:
                    return False
        return True

    def runCycle(self):
        # Tilt North
        self.tiltNorth()
        # Tilt West
        self.tiltWest()
        # Tilt South
        self.tiltSouth()
        # Tilt East
        self.tiltEast()

    def computeScore(self):
        totalScore=0
        # Score the grid
        for c,m in enumerate(self.map):
            # how many rocks are in this row?
            rocks=m.count("O")
            lineScore=rocks*(len(self.map)-c)
            totalScore+=lineScore

        return totalScore

map=[]


# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMapLine=list(lines[c])
    map.append(tempMapLine)
    print(map[-1])

originalDish=Dish(map)

print("**** DATA LOAD COMPLETE, starting run")
print("**** INITIAL MAP - taking a copy ****")
originalMap=[]
for i in range(0,len(originalDish.map)):
    originalMap.append(originalDish.map.copy())

cycles=1000000000
cycles=15
c=0

dishHistory=[]

print("MAP compare check:"+str(originalDish.compareMaps(originalDish.map)))

while True:
    originalDish.runCycle()
    c+=1
    same=False
    print("===> Running Cycle:"+str(c)+" Map score:"+str(originalDish.computeScore()))
    
    # Lets check the history to see if we have a cycle
    for historyIndex,h in enumerate(dishHistory):
        if h.compareMaps(originalDish.map):
            same=True
            break

    if same:
        print("**** REACHED SAME MAP **** After:"+str(c)+" original Map @ "+str(historyIndex))
        dishHistory[historyIndex].printMap()
        #break
    else:
        if c % 1000 == 0:
            print("**** MAP IS STILL DIFFERENT **** After:"+str(c))

    dishHistory.append(Dish(originalDish.map))

    if c == cycles:
        break
    
print("**** FINAL MAP ****")
originalDish.printMap()
print("**** Cycles Remainders:"+str(cycles%c))

totalScore=0
# Score the grid
for c,m in enumerate(originalDish.map):
    # how many rocks are in this row?
    rocks=m.count("O")
    lineScore=rocks*(len(originalDish.map)-c)
    print("Line "+str(c)+" has "+str(rocks)+" rocks, score="+str(lineScore))
    totalScore+=lineScore

# Print the final total score
print("Total Score = "+str(totalScore))

# Part 1 answer: 106378
# didnt cycle back to original map after; After:17953000 cycles
# After building a dish history stack, it does cycle back to the
# start after a reasonably small number (~100-150) of cycles, so its
# viable to mod this.
# TODO, I need to work out what the remainder is. Need to get my head
# around the fact that there is a start and end to the cycles that
# loop.