# https://www.redblobgames.com/pathfinding/a-star/introduction.html

from enum import Enum
import math
testing=True

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
        return result
    
    def customRestrictions(self,c):
        count=self.lastDirectionChange(c)
        if count>2:
            return False
        else:
            return True

    def getCardinalDirection(self,c1,c2):
        thisRow=c1[0]
        thisCol=c1[1]
        previousRow=c2[0]
        previousCol=c2[1]
        masterRowDelta=thisRow-previousRow
        masterColDelta=thisCol-previousCol

        if masterRowDelta==0 and masterColDelta>0:
            return Direction.East
        elif masterRowDelta==0 and masterColDelta<0:
            return Direction.West
        elif masterRowDelta>0 and masterColDelta==0:
            return Direction.South
        elif masterRowDelta<0 and masterColDelta==0:
            return Direction.North
        else:
            return Direction.NoDirection

    # Candidate format = [costToDate,row,col,fromRow,fromCol]
    def lastDirectionChange(self,c):
        thisRow=c[1]
        thisCol=c[2]
        previousRow=c[3]
        previousCol=c[4]
        masterRowDelta=thisRow-previousRow
        masterColDelta=thisCol-previousCol

        # print("Row Delta:"+str(masterRowDelta),end=" ")
        # print("Col Delta:"+str(masterColDelta),end=" ")
        count=0

        done=False
        while not done:
            count+=1
            thisRow=previousRow
            thisCol=previousCol
            previousRow=self.contents[thisRow][thisCol].backTrack[0]
            previousCol=self.contents[thisRow][thisCol].backTrack[1]
            # print("this Row:"+str(thisRow),end=" ")
            # print("this Col:"+str(thisCol),end=" ")

            nextRowDelta=thisRow-previousRow
            nextColDelta=thisCol-previousCol

            if thisRow==0 and thisCol==0:
                # We've reached the start of the path
                # print("Same directioin for:",count)
                return count

            if nextRowDelta==masterRowDelta and nextColDelta==masterColDelta:
                # Still heading in the same direction
                pass
            else:
                # We've changed direction, return the count
                # print("Same directioin for:",count)
                return count
            
        

    # TODO - I need to add the "cant travel in the same direction for more than 3 squares"
    # limitation, as well as only allowing to go right/left/forward.
    # Need some sort of direction history? Maybe backtrack along the matrix?

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
            elif self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar >= newLocationBeingLocked[0]:
                # the new path to this location is shorter than the current path
                # to this location, so this is a good candidate to test
                goodCandidateToTest=True
            else:
                #print("Dropping candidate:",newLocationBeingLocked)
                pass

        #print("Locking in candidate:",newLocationBeingLocked)

        # Lets update the current location based on this new candidate as it looks good
        self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].visited=True
        self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar=newLocationBeingLocked[0]
        self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].backTrack=[newLocationBeingLocked[3],newLocationBeingLocked[4]]

        if self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].visited==True and self.contents[newLocationBeingLocked[3]][newLocationBeingLocked[4]].backTrack==None:
            print("ERROR - no backtrack for:",newLocationBeingLocked)
            print("*** Tried to set it to:",[newLocationBeingLocked[1],newLocationBeingLocked[2]])


        # PART 2: Generate new candidates for the next step in the path

        # Check each of the neighbours to see if we are able to treat it as a next step
        # in the path.
        neighbours=[[0,-1],[0,+1],[-1,0],[+1,0]]
        for n in neighbours:

            # Does this candidate match the custom restrictions
            if self.customRestrictions(newLocationBeingLocked)==False:
                # this does not, so drop it from the list
                print("Dropping candidate:",n)
                continue

            # Based on the new location that we're locking in, lets generate a new candidate
            # list.
            candidateRow=newLocationBeingLocked[1]+n[0]
            candidateCol=newLocationBeingLocked[2]+n[1]
            if candidateRow>=0 and candidateRow<len(self.contents) and candidateCol>=0 and candidateCol<len(self.contents[0]):

                # set the path cost to this point equal to the previous candidate
                # cost path plus this candidate additional weight
                newCostSoFar=self.contents[candidateRow][candidateCol].weight+self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar
                #print("New candidate cost so far:",newCostSoFar,self.contents[candidateRow][candidateCol].weight,self.contents[newLocationBeingLocked[1]][newLocationBeingLocked[2]].costSoFar)

                # Lets only add this as a candidate if we know that the path to the new location is better than
                # any previous path that visited it:
                if self.contents[candidateRow][candidateCol].visited==False or self.contents[candidateRow][candidateCol].costSoFar > newCostSoFar:
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
doneSearchingForPath=False

print("**** RUN COMPLETE, final state is:")
total=0
print("Total is: "+str(total))

import pygame, sys, random
from pygame.locals import *
pygame.init()

# Colours
BACKGROUND = (255, 255, 255)
# Initializing Color
red = (255,0,0)
green= (0,255,0)
blue= (0,0,255)
yellow = (255,255,0)

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

bigFont = pygame.font.SysFont(None, math.floor(scale/2))
smallFont = pygame.font.SysFont(None, math.floor(scale/4))

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



    if not doneSearchingForPath:
        s+=1
        map.searchPath()

        doneSearchingForPath=True
        if len(map.currentCandidateList)!=0:
            doneSearchingForPath=False

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
                pygame.draw.line(WINDOW, red, (x*scale, y*scale), (c.backTrack[1]*scale, c.backTrack[0]*scale))

                smallText="W:"+str(map.contents[y][x].weight)+" C:"+str(map.contents[y][x].costSoFar)
                fImage = smallFont.render(smallText, True, blue)
                WINDOW.blit(fImage, (x*scale, (y*scale)+math.floor(scale/2)))

    for c in map.currentCandidateList:
        pygame.draw.rect(WINDOW, yellow, pygame.Rect(c[2]*scale, c[1]*scale, scale, scale))


    # This bit of code we want to run only once after we've finished searchig for
    # for a path, because we want to be able to leave the final screen being repeatedly
    # redrawn without constantly recomputing the shortest path
    if doneSearchingForPath and runOnce:
        sPath=map.getShortestPathToTarget()
        sPath.reverse()

        for i,c in enumerate(sPath):
            print(c,end=" ")
            if i<len(sPath)-1:
                print(map.getCardinalDirection(sPath[i+1],sPath[i]))

        tRow=len(map.contents)-1
        tCol=len(map.contents[0])-1
        print("Target is:",map.contents[tRow][tCol].costSoFar)
        runOnce=False


    if doneSearchingForPath:
        oldC=sPath[0]
        for i,c in enumerate(sPath):
            # draw a line from centre of current cell, to the centre of the cell stored in the value of "C"
            #pygame.draw.line(WINDOW, (0,0,255), (oldC[1]*scale+hScale, oldC[0]*scale+hScale), (c[1]*scale+hScale, c[0]*scale+hScale))
            pygame.draw.line(WINDOW, blue, (oldC[1]*scale, oldC[0]*scale), (c[1]*scale, c[0]*scale))
            pygame.draw.rect(WINDOW, yellow, pygame.Rect(c[1]*scale, c[0]*scale, scale, scale))

            if i<len(sPath)-1:
                dir=map.getCardinalDirection(sPath[i+1],sPath[i])

                fImage = bigFont.render(dir.name, True, blue)
                WINDOW.blit(fImage, (c[1]*scale, c[0]*scale))

                smallText="W:"+str(map.contents[sPath[i][0]][sPath[i][1]].weight)+" C:"+str(map.contents[sPath[i][0]][sPath[i][1]].costSoFar)

                #smallText="W:"+str(map.contents[sPath[i][0]][sPath[i][1]].weight)
                fImage = smallFont.render(smallText, True, blue)
                WINDOW.blit(fImage, (c[1]*scale, (c[0]*scale)+math.floor(scale/2)))


            oldC=c


    #pygame.display.flip()

    pygame.display.update()
    fpsClock.tick(FPS)