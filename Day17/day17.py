# https://www.redblobgames.com/pathfinding/a-star/introduction.html

from enum import Enum
import math
testing=False

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
if testing:
    file1 = open('Day17/data/input_test.txt', 'r')
    lines = file1.readlines()
else:
    file1 = open('Day17/data/input.txt', 'r')
    lines = file1.readlines()

class CellContents:
    def __init__(self,w):
        self.weight=w
        self.costSoFar=0
        self.backTrack=None
        self.visited=False

    def print(self):
        print("Weight:"+str(self.weight),end="")
        print(" Cost:"+str(self.costSoFar),end="")
        print(" BackTrack:"+str(self.backTrack),end="")
        print(" Visited:"+str(self.visited))

class Grid:
    def __init__(self,lines):
        self.contents=[]
        # Loop through the text input converting to the map
        # as we parse
        for c,l in enumerate(lines):
            lines[c]=lines[c].strip()
            tempMapLine=list(lines[c])

            # Convert all the values in the line into ints
            for c,w in enumerate(tempMapLine):
                tempMapLine[c]=CellContents(int(w))

            self.contents.append(tempMapLine)

        self.targetRow=len(self.contents)
        self.targetCol=len(self.contents[0])

        # Treat currentCandidateList as a hashmap - we create a seperate list
        # for each candidate who has a cost score 1-9
        self.currentCandidateList=[]

        self.targetFound=False

    def printMap(self,s):
        print("** "+s+" **")
        for r in range(len(self.contents)):
            for c in range(len(self.contents[r])):
                print(self.contents[r][c].weight,end="")
            print()

    def getShortestPathToTarget(self):
        result=[]

        # start with a default "end" position
        # of the bottom/right square (this looks
        # like its working)
        tRow=len(self.contents)-1
        tCol=len(self.contents[0])-1
        result.append([tRow,tCol])
        print("Adding:"+str(tRow)+","+str(tCol))


        done=False
        while not done:
            if self.contents[tRow][tCol].backTrack==None:
                break

            newTRow=self.contents[tRow][tCol].backTrack[0]
            newTCol=self.contents[tRow][tCol].backTrack[1]
            print("Adding:"+str(newTRow)+","+str(newTCol))
            result.append([newTRow,newTCol])

            if newTRow<=0 and newTCol<=0:
                done=True
                
            tRow=newTRow
            tCol=newTCol
        return(result)
    
    # TODO - I need to add the "cant travel in the same direction for more than 3 squares"
    # limitation, as well as only allowing to go right/left/forward.
    # Need some sort of direction history? Maybe backtrack along the matrix?
    # TODO - rewrite the candidate list to use the new CellContents format, add in the
    # total path cost, and redo the candidate sorting based on total path cost    


    # Candidate format = [costToDate,row,col,fromRow,fromCol]
    def searchPath(self):

        # PART 1: Lock in the new more favoured candidate

        goodCandidateToTest=False
        # We need to find a candidate that leads to a space we've either not visited
        # or one that will visit a square that has already been visited, but via
        # a shorter path, so is this a good candidate to test, or should we just
        # drop it?
        while not goodCandidateToTest:
            # if we've run out of candidates then return
            if len(self.currentCandidateList)==0:
                return
            # if we've got a candidate in the list, save it and pop it off the list            
            newLocationBeingLocked=self.currentCandidateList.pop(0)

            # is this a good candidate though?
            if self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].visited==False:
                # we haven't visited this location, so by default this is a good one to visit
                goodCandidateToTest=True
            elif self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar > newLocationBeingLocked[0]:
                # the new path to this location is shorter than the current path
                # to this location, so this is a good candidate to test
                goodCandidateToTest=True
            else:
                print("Dropping candidate:",newLocationBeingLocked)


        print("Locking in candidate:",newLocationBeingLocked)

        # Lets update the current location based on this new candidate as it looks good
        self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].visited=True
        self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar=newLocationBeingLocked[0]
        self.contents[newLocationBeingLocked[3]][newLocationBeingLocked[4]].backTrack=[newLocationBeingLocked[1],newLocationBeingLocked[2]]

        if self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].visited==True and self.contents[newLocationBeingLocked[3]][newLocationBeingLocked[4]].backTrack==None:
            print("ERROR - no backtrack for:",newLocationBeingLocked)
            print("*** Tried to set it to:",[newLocationBeingLocked[1],newLocationBeingLocked[2]])


        # PART 2: Generate new candidates for the next step in the path

        # Check each of the neighbours to see if we are able to treat it as a next step
        # in the path.
        neighbours=[[0,-1],[0,+1],[-1,0],[+1,0]]
        for n in neighbours:

            # Based on the new location that we're locking in, lets generate a new candidate
            # list.
            candidateRow=newLocationBeingLocked[1]+n[0]
            candidateCol=newLocationBeingLocked[2]+n[1]
            if candidateRow>=0 and candidateRow<len(self.contents) and candidateCol>=0 and candidateCol<len(self.contents[0]):

                # set the path cost to this point equal to the previous candidate
                # cost path plus this candidate additional weight
                newCostSoFar=self.contents[candidateRow][candidateCol].weight+self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar
                print("New candidate cost so far:",newCostSoFar,self.contents[candidateRow][candidateCol].weight,self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar)

                # Lets only add this as a candidate if we know that the path to the new location is better than
                # any previous path that visited it:
                if self.contents[candidateRow][candidateCol].visited==False:
                    self.currentCandidateList.append([newCostSoFar,candidateRow,candidateCol,newLocationBeingLocked[1],newLocationBeingLocked[2]])
                elif self.contents[candidateRow][candidateCol].costSoFar > newCostSoFar:
                    self.currentCandidateList.append([newCostSoFar,candidateRow,candidateCol,newLocationBeingLocked[1],newLocationBeingLocked[2]])

        # # New candidate list now needs to be sorted
        # print("Candidate list is: ",self.currentCandidateList)
        self.currentCandidateList.sort()
        # print("Sorted candidate list is: ",self.currentCandidateList)



map=Grid(lines)
map.printMap("Initial State")
print("**** DATA LOAD COMPLETE, starting run")

print("valid paths test:")
w=map.contents[0][0].weight
map.currentCandidateList.append([w,0,0,0,0])
s=0
maxSteps=100

#for s in range(maxSteps):
done=False

print("**** RUN COMPLETE, final state is:")
total=0
print("Total is: "+str(total))

import pygame, sys, random
from pygame.locals import *
pygame.init()

# Colours
BACKGROUND = (255, 255, 255)
 
# Game Setup
FPS = 60
if testing:
    scale=50
else:
    scale=5

hScale=math.ceil(scale/2)

fpsClock = pygame.time.Clock()
WINDOW_WIDTH = map.targetCol*scale
WINDOW_HEIGHT = map.targetRow*scale
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AoC Display')


# Render elements of the game
WINDOW.fill(BACKGROUND)

runOnce=True
looping=True
 # The main game loop
while looping:
    # Get inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Initializing Color
    red = (255,0,0)
    green= (0,255,0)
    blue= (0,0,255)
    

    if not done:
        s+=1
        map.searchPath()

        done=True
        if len(map.currentCandidateList)!=0:
            done=False

    # Main draw loop
    for y,l in enumerate(map.contents):
        for x,c in enumerate(l):

            g=math.floor(128/(map.contents[y][x].weight+1))+127
            if c.visited==False:
                pygame.draw.rect(WINDOW, (g,g,g), pygame.Rect(x*scale, y*scale, scale, scale))
            else:
                pygame.draw.rect(WINDOW, (0,g,0), pygame.Rect(x*scale, y*scale, scale, scale))
                # draw a line from the centre of this cell, to the centre of the cell stored in the value of "C"
                #print(c)
                #pygame.draw.line(WINDOW, (255,0,0), (x*scale+hScale, y*scale+hScale), (c[1]*scale+hScale, c[0]*scale+hScale))

            if c.backTrack!=None:
                pygame.draw.line(WINDOW, (255,0,0), (x*scale, y*scale), (c.backTrack[1]*scale, c.backTrack[0]*scale))

    for c in map.currentCandidateList:
        pygame.draw.rect(WINDOW, (255,255,0), pygame.Rect(c[2]*scale, c[1]*scale, scale, scale))


    if done and runOnce:
        # TODO - I think there is some bugs with the drawing here, as it goes diagonal across blocks some times. I'm taking it on faith
        # that CW got the co-ords right as well. (tbf - they do look consistent with above)
        sPath=map.getShortestPathToTarget()
        for c in sPath:
            print(c)

        runOnce=False

        for r in range(len(map.contents)):
            for c in range(len(map.contents[r])):
                print("R/C:"+str(r)+"/"+str(c),end=" ")
                map.contents[r][c].print()

    if not runOnce:
        oldC=sPath[0]
        for c in sPath:
            # draw a line from centre of current cell, to the centre of the cell stored in the value of "C"
            #pygame.draw.line(WINDOW, (0,0,255), (oldC[1]*scale+hScale, oldC[0]*scale+hScale), (c[1]*scale+hScale, c[0]*scale+hScale))
            pygame.draw.line(WINDOW, (0,0,255), (oldC[1]*scale, oldC[0]*scale), (c[1]*scale, c[0]*scale))

            oldC=c


    #pygame.display.flip()

    pygame.display.update()
    fpsClock.tick(FPS)