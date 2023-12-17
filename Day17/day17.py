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
            for c,t in enumerate(tempMapLine):
                tempMapLine[c]=int(t)
            self.map.append(tempMapLine)
            self.trace.append([0] * len(tempMapLine))

        self.printMap("Map Init")

        self.startRow=0
        self.startCol=0
        self.direction=0
        self.targetRow=len(self.map)
        self.targetCol=len(self.map[0])

        self.currentCandidateList=[]

        self.targetFound=False

    def printMap(self,s):
        print("** "+s+" **")
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                print(self.map[r][c],end="")
            print()

    def printTrace(self,s):
        print("** "+s+" **")
        for r in range(len(self.trace)):
            for c in range(len(self.trace[r])):
                print(self.trace[r][c],end="")
            print()

    def initPath(self,sRow,sCol,d,tRow,tCol):
        self.startRow=sRow
        self.startCol=sCol
        self.direction=d
        self.targetRow=tRow
        self.targetCol=tCol
        self.currentCandidateList.append((self.startRow,self.startCol,self.direction,0))


    def stepPath(self):
        print("*** Current Candidate List: "+str(len(self.currentCandidateList)))
        tempCandidateList=[]

        # Lets check each candidate in the current list and work out if there
        # is a valid next step it could do. We work backwards through the list,
        # so that we can pop the current element from the list before adding
        # anything new to the list, thus ensuring list integrity
        for c in self.currentCandidateList:
            print(c)

            # set the cell in the tracker to indicate we've hit this cell by adding
            # the current weight to it
            self.trace[c[0]][c[1]]=c[3]

            if c[0]==self.targetRow and c[1]==self.targetCol:
                # we have found the target, lets print out the trace state
                self.printTrace("Target Found")
                self.targetFound=True

            newPossibleCandidateDirections=self.potentialAllowedMoves(c)
            
            # Lets just save all the new candidates to a list and we'll sort them out
            # once we're done with the pass of the current candidates
            for d in newPossibleCandidateDirections:
                nextStep=self.testMove(c,d)
                #print("Checking Possible New Candidates:",end="")
                #print(nextStep)
                if nextStep==None:
                    pass
                else:
                    if self.trace[nextStep[0]][nextStep[1]]>0:
                        pass
                    tempCandidateList.append(nextStep)

        self.currentCandidateList.clear()
        self.currentCandidateList=tempCandidateList.copy()


    def potentialAllowedMoves(self,c):
        d=c[2] # get the direction of the current candidate
        allowedMoves=[]
        # we are only allowed to move forward (if we've changed direction within the last 2 moves)
        # otherwise we must turn/move into the square to the right or the left. First of all
        # lets work out the left/right options
        if d==Direction.North or d==Direction.South:
            allowedMoves.append(Direction.East)
            allowedMoves.append(Direction.West)
        elif d==Direction.East or d==Direction.West:
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
        allowedMoves.append(d)
        
        return allowedMoves
    
    def testMove(self,candidate, d):

        r=candidate[0]
        c=candidate[1]

        if d==Direction.North:
            r-=1
        elif d==Direction.East:
            c+=1
        elif d==Direction.South:
            r+=1
        elif d==Direction.West:
            c-=1

        if r<0 or r>=len(self.map):
            return None
        if c<0 or c>=len(self.map[r]):
            return None
        
        # Already visited - possible TODO - we might need to rework
        # this and replace this entry if we think the current one would
        # be better
        if self.trace[r][c]!=0:
            return None

        return (r,c,d,candidate[3]+self.map[r][c])
    
    def distanceToTarget(self):
        return abs(self.targetRow-self.startRow)+abs(self.targetCol-self.startCol)



map=Map(lines)
map.printMap("Initial State")
print("**** DATA LOAD COMPLETE, starting run")

print("valid paths test:")

# calculate the index of the bottom right cell of the map
tRow=len(map.map)-1
tCol=len(map.map[tRow])

map.initPath(0,0,Direction.East,tRow,tCol)

s=0
maxSteps=600
while map.targetFound==False and s<maxSteps:    
    map.stepPath()
    s+=1
    map.printTrace("Step "+str(s))

print("**** RUN COMPLETE, final state is:")
total=0

print("Total is: "+str(total))
