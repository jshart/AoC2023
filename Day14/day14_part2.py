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
for currentCycleCount,l in enumerate(lines):
    lines[currentCycleCount]=lines[currentCycleCount].strip()
    tempMapLine=list(lines[currentCycleCount])
    map.append(tempMapLine)
    print(map[-1])

activeDish=Dish(map)

print("**** DATA LOAD COMPLETE, starting run")
print("**** INITIAL MAP - taking a copy ****")
originalMap=[]
for i in range(0,len(activeDish.map)):
    originalMap.append(activeDish.map.copy())

cycles=1000000000
#cycles=15
currentCycleCount=0

dishHistory=[]

print("MAP compare check:"+str(activeDish.compareMaps(activeDish.map)))

while True:
    activeDish.runCycle()
    currentCycleCount+=1
    same=False
    print("===> Running Cycle:"+str(currentCycleCount)+" Map score:"+str(activeDish.computeScore()))
    
    # Lets check the history to see if we have a cycle
    for historyIndex,h in enumerate(dishHistory):
        if h.compareMaps(activeDish.map):
            same=True
            break

    if same:
        print("**** REACHED SAME MAP **** After:"+str(currentCycleCount)+" original Map @ "+str(historyIndex))
        dishHistory[historyIndex].printMap()
        unrepeatedStart=historyIndex-1
        rangeOfRepeatedSection=currentCycleCount-unrepeatedStart
        zoneWhichMayRepeat=cycles-unrepeatedStart

        #TODO - this is still bugged, need to spend some more time thinking about these parts
        #TODO - I think our CycleCount beginning at 1 is messing up the indexing into history
        # map, as we add stuff as a stack, so first element will be 0 and not 1

        partialRepeatAtEnd=zoneWhichMayRepeat%rangeOfRepeatedSection
        print("unrepeatedStart = "+str(unrepeatedStart),end=" ")
        print("rangeOfRepeatedSection = "+str(rangeOfRepeatedSection),end=" ")
        print("zoneWhichMayRepeat = "+str(zoneWhichMayRepeat),end=" ")
        print("indexIntoRepeatedSection = "+str(partialRepeatAtEnd))
        break
    else:
        if currentCycleCount % 1000 == 0:
            print("**** MAP IS STILL DIFFERENT **** After:"+str(currentCycleCount))

    dishHistory.append(Dish(activeDish.map))

    if currentCycleCount == cycles:
        break
    
print("**** FINAL MAP ****")
print("**** Checking which map we end on based on:"+str(partialRepeatAtEnd))
finalMap=dishHistory[unrepeatedStart+partialRepeatAtEnd]
finalMap.printMap()
totalScore=0
# Score the grid
for currentCycleCount,m in enumerate(finalMap.map):
    # how many rocks are in this row?
    rocks=m.count("O")
    lineScore=rocks*(len(finalMap.map)-currentCycleCount)
    print("Line "+str(currentCycleCount)+" has "+str(rocks)+" rocks, score="+str(lineScore))
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