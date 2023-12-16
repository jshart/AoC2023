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
file1 = open('Day16/data/input.txt', 'r')
lines = file1.readlines()

map=[]
energyState=[]

def scoreEnergyState(e):
    score=0
    for r in range(len(e)):
        for c in range(len(e[r])):
            for s in range(len(e[r][c])):
                if e[r][c][s] in "#<>v^":
                    score+=1
                    break
    return score

def printMap(m,s):
    print("** "+s+" **")
    for r in range(len(m)):
        for c in range(len(m[r])):
            print(m[r][c][-1],end="")
        print()

class Photon:
    def __init__(self,startRow,startCol,startDirection):
        self.row=startRow
        self.col=startCol
        self.direction=startDirection

    def directionAsASCII(self):
        if self.direction==Direction.North:
            return "^"
        elif self.direction==Direction.East:
            return ">"
        elif self.direction==Direction.South:
            return "v"
        elif self.direction==Direction.West:
            return "<"

    def resetPositionAfterSplit(self):
        if self.direction==Direction.North:
            self.row-=1
        elif self.direction==Direction.East:
            self.col+=1
        elif self.direction==Direction.South:
            self.row+=1
        elif self.direction==Direction.West:
            self.col-=1

        if self.row<0 or self.row>=len(map) or self.col<0 or self.col>=len(map[0]):
            self.direction=Direction.Stopped

    def printState(self,n):
        print("Thread:"+str(n)+" row: "+str(self.row)+" col: "+str(self.col)+" direction: "+str(self.direction))

    def move(self,map,eMap):

        returnDirection=Direction.NoDirection

        if self.direction==Direction.Stopped:
            return Direction.Stopped

        if map[self.row][self.col]=="/":
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
            state=(self.row,self.col,self.direction)
            if self.directionAsASCII() in eMap[self.row][self.col]:
                self.direction=Direction.Stopped
            else:
                if self.direction==Direction.North:
                    eMap[self.row][self.col]+="^"
                elif self.direction==Direction.East:
                    eMap[self.row][self.col]+=">"
                elif self.direction==Direction.South:
                    eMap[self.row][self.col]+="v"
                elif self.direction==Direction.West:
                    eMap[self.row][self.col]+="<"
                else:
                    eMap[self.row][self.col]+="#"

        return returnDirection

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMapLine=list(lines[c])
    map.append(tempMapLine)

for r in enumerate(map):
    energyState.append(["."] * len(map[0]))


printMap(map,"Initial State")
print("**** DATA LOAD COMPLETE, generate run list")

startPositions=[]
# lets check each element around the edges of the map and build a list of
# run locations
for c in range(len(map)):
    # lets check the top row
    if map[0][c]==".":
        startPositions.append((0,c,Direction.South))

    if map[len(map)-1][c]==".":
        startPositions.append((len(map)-1,c,Direction.North))

for c in range(len(map[0])):
    # lets check the top row
    if map[c][0]==".":
        startPositions.append((c,0,Direction.East))

    if map[c][len(map)-1]==".":
        startPositions.append((c,len(map)-1,Direction.West))


highestTotal=0
for startPosition in startPositions:
    # for s in startPositions:
    #     energyState[s[0]][s[1]]="*"

    # printMap(energyState,"start positions")
    steps=10
    allStopped=False

    # we need to scrub the energyState so its ready for the next run
    for r in range(len(energyState)):
        for c in range(len(energyState[r])):
            energyState[r][c]="."

    photons=[]
    photons.append(Photon(startPosition[0],startPosition[1],startPosition[2]))
    energyState[0][0]="#"

    run=0
    maxRuns=1000
    allDone=False
    while not allDone:

        # Lazy code, but just to make things easier, lets first remove any
        # stopped threads
        for i in range(len(photons)-1,-1,-1):   
            if photons[i].direction==Direction.Stopped:
                #print("Removing thread as it stopped:"+str(i))
                del photons[i]

        for threadNum,p in enumerate(photons):
            splitDirection=p.move(map,energyState)

            # This is not stopped, if it is however set to a direction
            # then that means we should split the photon into two
            if splitDirection!=Direction.NoDirection:
                newPhoton=Photon(p.row,p.col,splitDirection)
                newPhoton.resetPositionAfterSplit()

                photons.append(newPhoton)

        run+=1
        #print("Run:"+str(run)+" Total threads:"+str(len(photons))+" Total Energized:"+str(scoreEnergyState(energyState)))
        
        allStopped=True
        for p in photons:
            if p.direction!=Direction.Stopped:
                allStopped=False
                break
            
        if allStopped:
            allDone=True
            print("**** Exiting due to all threads stopped****")

        if run>=maxRuns:
            allDone=True
            print("**** Exiting due to too many Runs ****")
            pass

    print("**** RUN COMPLETE, final state is:")
    total=0

    printMap(energyState,"Energy State")
    print("Final energy state score:"+str(scoreEnergyState(energyState)))
    
    if scoreEnergyState(energyState)>highestTotal:
        highestTotal=scoreEnergyState(energyState)
        print("New Highest Total:"+str(highestTotal))

print("Final and Highest Total:"+str(highestTotal))