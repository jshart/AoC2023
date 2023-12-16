from enum import Enum

# create an enum for the compass cardinal directions
class Direction(Enum):
    Stopped=0
    North=1
    East=2
    South=3
    West=4
    NoDirection=5


# load a text file
# read file input.txt into an array of strings
file1 = open('Day16/data/input_test.txt', 'r')
lines = file1.readlines()

map=[]
energyState=[]
oldEnergyState=[]

def copyEnergyState(source, dest):
    for r in range(len(source)):
        for c in range(len(source[r])):
            dest[r][c]=source[r][c]

def compareEnergyStates(source, dest):
    for r in range(len(source)):
        for c in range(len(source[r])):
            if dest[r][c]!=source[r][c]:
                return False
        
    print("Energy states are the same")
    return True

def printMap(m,s):
    print("** "+s+" **")
    for r in range(len(m)):
        for c in range(len(m[r])):
            print(m[r][c],end="")
        print()

class Photon:
    def __init__(self,startRow,startCol,startDirection):
        self.row=startRow
        self.col=startCol
        self.direction=startDirection

    def printState(self,n):
        print("Thread:"+str(n)+" row: "+str(self.row)+" col: "+str(self.col)+" direction: "+str(self.direction))

    def move(self,map,eMap):

        returnDirection=Direction.NoDirection

        if self.direction==Direction.Stopped:
            return Direction.Stopped



        if map[self.row][self.col]=="#":
            # No mirror, but already energeised so just keep going
            pass
        elif map[self.row][self.col]==".":
            # No mirror, and unenergised so lets energise
            eMap[self.row][self.col]="#"
        elif map[self.row][self.col]=="/":
            if self.direction==Direction.North:
                self.direction=Direction.East
            elif self.direction==Direction.East:
                self.direction=Direction.North
            elif self.direction==Direction.South:
                self.direction=Direction.West
            elif self.direction==Direction.West:
                self.direction=Direction.South
        elif map[self.row][self.col]=="\\":
            if self.direction==Direction.North:
                self.direction=Direction.West
            elif self.direction==Direction.East:
                self.direction=Direction.South
            elif self.direction==Direction.South:
                self.direction=Direction.East
            elif self.direction==Direction.West:
                self.direction=Direction.North
        elif map[self.row][self.col]=="-":
            if self.direction==Direction.North:
                returnDirection=Direction.West
                self.direction=Direction.East
            elif self.direction==Direction.South:
                returnDirection=Direction.West
                self.direction=Direction.East
        elif map[self.row][self.col]=="|":
            if self.direction==Direction.East:
                returnDirection=Direction.South
                self.direction=Direction.North
            elif self.direction==Direction.West:
                returnDirection=Direction.South
                self.direction=Direction.North

        # Depending on which direction 
        # we are travelling we increase
        # or decrease the row or column
        # accordingly
        if self.direction==Direction.North:
            self.row-=1
        elif self.direction==Direction.East:
            self.col+=1
        elif self.direction==Direction.South:
            self.row+=1
        elif self.direction==Direction.West:
            self.col-=1

        # if the photon is outside the bounds
        # of the grid, then we just set it to
        # stopped
        if self.row<0 or self.row>=len(map) or self.col<0 or self.col>=len(map[0]):
            self.direction=Direction.Stopped
        else:
            eMap[self.row][self.col]="#"


        return returnDirection


photons=[]
photons.append(Photon(0,0,Direction.East))

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMapLine=list(lines[c])
    map.append(tempMapLine)

for r in enumerate(map):
    energyState.append(["."] * len(map[0]))
    oldEnergyState.append(["."] * len(map[0]))



printMap(map,"Initial State")
print("**** DATA LOAD COMPLETE, starting run")
steps=10
allStopped=False
#for i in range(steps):

run=0
maxRuns=200
allDone=False
while not allDone:

    # Lazy code, but just to make things easier, lets first remove any
    # stopped threads
    for i in range(len(photons)-1,-1,-1):   
        if photons[i].direction==Direction.Stopped:
            print("Removing thread:"+str(i))
            del photons[i]

    # Copy Energy State
    copyEnergyState(energyState,oldEnergyState)

    for threadNum,p in enumerate(photons):
        splitDirection=p.move(map,energyState)

        # This is not stopped, if it is however set to a direction
        # then that means we should split the photon into two
        if splitDirection!=Direction.NoDirection:
            print("Split, new photon:"+str(splitDirection))
            newPhoton=Photon(p.row,p.col,splitDirection)
            photons.append(newPhoton)

        p.printState(threadNum)

    run+=1
    printMap(energyState,"Run:"+str(run))

    # Any update to the energy state on this run?
    if compareEnergyStates(oldEnergyState,energyState):
        allDone=True
        print("**** Exiting due to no change in energy state****")

    if run>=maxRuns:
        allDone=True
        print("**** Exiting due to too many Runs ****")
        

print("**** RUN COMPLETE, final state is:")
total=0

print("Total Energized is: "+str(total))

printMap(energyState,"Energy State")
printMap(oldEnergyState,"Old Energy State")


# TODO - need to solve the problem of photons boucing along the same
# paths and thus not showing any updates to the energy states - makes
# it difficult to identify the exit case.