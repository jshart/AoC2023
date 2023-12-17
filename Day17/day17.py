# https://www.redblobgames.com/pathfinding/a-star/introduction.html

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
file1 = open('Day17/data/input_test.txt', 'r')
lines = file1.readlines()

class Map:
    def __init__(self,lines):
        self.map=[]
        self.trace=[]
        for c,l in enumerate(lines):
            lines[c]=lines[c].strip()
            tempMapLine=list(lines[c])
            self.map.append(tempMapLine)
            self.trace.append([0] * len(tempMapLine))


        self.row=len(self.map)
        self.col=len(self.map[0])
        self.printMap("Map Init")
        self.currentPath=None

    def printMap(self,s):
        print("** "+s+" **")
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                print(self.map[r][c],end="")
            print()

    def initPath(self,sRow,sCol,d,tRow,tCol):
        self.currentPath=Path(sRow,sCol,d,tRow,tCol)


class Path:
    def __init__(self,startRow,startCol,startDirection,targetRow,targetCol):
        self.row=startRow
        self.col=startCol
        self.direction=startDirection
        # self.history=[]
        # self.history.append((self.row,self.col,self.direction))
        self.targetRow=targetRow
        self.targetCol=targetCol

    def printState(self):
        print("Row: "+str(self.row)+" col: "+str(self.col)+" direction: "+str(self.direction))

    def nextAllowedMoves(self):
        allowedMoves=[]
        # we are only allowed to move forward (if we've changed direction within the last 2 moves)
        # otherwise we must turn/move into the square to the right or the left. First of all
        # lets work out the left/right options
        if self.direction==Direction.North or self.direction==Direction.South:
            allowedMoves.append(Direction.East)
            allowedMoves.append(Direction.West)
        elif self.direction==Direction.East or self.direction==Direction.West:
            allowedMoves.append(Direction.North)
            allowedMoves.append(Direction.South)
        
        # If we've travelled 3 spaces in the same direction then only the above
        # moves are valid, as we must turn, however if we've not travelled 3 spaces
        # in the same direction then we can add the current direction to the valid
        # next path locations.
        # mustChangeDirection=False
        # if len(self.history)>=3:
        #     if self.history[-1][2]==self.history[-2][2] and self.history[-1][2]==self.history[-3][2]:
        #         mustChangeDirection=True
        
        # if not mustChangeDirection:
        allowedMoves.append(self.direction)
        
        return allowedMoves
    
    def testMove(self,map,d):

        r=self.row
        c=self.col

        if d==Direction.North:
            r-=1
        elif d==Direction.East:
            c+=1
        elif d==Direction.South:
            r+=1
        elif d==Direction.West:
            c-=1

        if r<0 or r>=len(map):
            return None
        if c<0 or c>=len(map[r]):
            return None

        return (r,c,d)
    
    def distanceToTarget(self):
        return abs(self.targetRow-self.row)+abs(self.targetCol-self.col)



map=Map(lines)
map.printMap("Initial State")
print("**** DATA LOAD COMPLETE, starting run")

print("valid paths test:")

# calculate the index of the bottom right cell of the map
tRow=len(map.map)-1
tCol=len(map.map[tRow])

map.initPath(0,0,Direction.East,tRow,tCol)
moves=map.currentPath.nextAllowedMoves()
for m in moves:
    print(str(m),end=",")
    print(str(map.currentPath.testMove(map.map,m)))

print("**** RUN COMPLETE, final state is:")
total=0

print("Total is: "+str(total))
