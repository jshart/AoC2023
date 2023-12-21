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

# TODO - I need to add the "cant travel in the same direction for more than 3 squares"
# limitation, as well as only allowing to go right/left/forward.
# Need some sort of direction history? Maybe backtrack along the trace matrix?
def searchPath(m,v):
    # find the lowest number candidate
    for hashCandidates in map.currentCandidateList:
        if len(hashCandidates)>0:
            candidate = hashCandidates.pop(0)
            break

    # Check each of the neighbours to see if we are able to treat it as a next step
    # in the path.
    neighbours=[[0,-1],[0,+1],[-1,0],[+1,0]]
    for n in neighbours:
        row=candidate[0]+n[0]
        col=candidate[1]+n[1]
        if row>=0 and row<len(m.trace) and col>=0 and col<len(m.trace[0]):
            # Have we visited this cell before?
            if m.trace[row][col]==0:
                # if not, track the path to this cell
                m.trace[row][col]=candidate
                # create a new candidate list for this cell
                newCandidate=[row,col]
                # get the weight from the map
                v=m.costMap[row][col]
                # is this candidate alread in the hashmap?
                if newCandidate not in map.currentCandidateList[v]:
                    # it isn't so add it.
                    map.currentCandidateList[v].append(newCandidate)
            

# load a text file
# read file input.txt into an array of strings
if testing:
    file1 = open('Day17/data/input_test.txt', 'r')
    lines = file1.readlines()
else:
    file1 = open('Day17/data/input.txt', 'r')
    lines = file1.readlines()

class Map:
    def __init__(self,lines):
        self.costMap=[]
        self.trace=[]
        #self.costToReach=[]
        for c,l in enumerate(lines):
            lines[c]=lines[c].strip()
            tempMapLine=list(lines[c])
            for c,t in enumerate(tempMapLine):
                tempMapLine[c]=int(t)
            self.costMap.append(tempMapLine)
            self.trace.append([0] * len(tempMapLine))
            #self.costToReach.append([0] * len(tempMapLine))

        self.targetRow=len(self.costMap)
        self.targetCol=len(self.costMap[0])

        # Treat currentCandidateList as a hashmap - we create a seperate list
        # for each candidate who has a cost score 1-9
        self.currentCandidateList=c=[[] for x in range(10)]

        self.targetFound=False

    def printMap(self,s,m):
        print("** "+s+" **")
        for r in range(len(m)):
            for c in range(len(m[r])):
                print(m[r][c],end="")
            print()

    def getShortestPathToTarget(self):
        result=[]

        # start with a default "end" position
        # of the bottom/right square (this looks
        # like its working)
        tRow=len(map.trace)-1
        tCol=len(map.trace[0])-1
        result.append([tRow,tCol])
        print("Adding:"+str(tRow)+","+str(tCol))


        done=False
        while not done:
            newTRow=map.trace[tRow][tCol][0]
            newTCol=map.trace[tRow][tCol][1]
            print("Adding:"+str(newTRow)+","+str(newTCol))
            result.append([newTRow,newTCol])

            if newTRow<=0 and newTCol<=0:
                done=True
                
            tRow=newTRow
            tCol=newTCol
        return(result)


map=Map(lines)
map.printMap("Initial State",map.costMap)
print("**** DATA LOAD COMPLETE, starting run")

print("valid paths test:")
map.currentCandidateList[map.costMap[0][0]].append([0,0])
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
        searchPath(map,s)

        done=True
        for c in map.currentCandidateList:
            if len(c)>0:
                done=False
                break

    # Main draw loop
    for y,l in enumerate(map.trace):
        for x,c in enumerate(l):

            g=math.floor(128/(map.costMap[y][x]+1))+127
            if c==0:
                pygame.draw.rect(WINDOW, (g,g,g), pygame.Rect(x*scale, y*scale, scale, scale))
            else:
                pygame.draw.rect(WINDOW, (0,g,0), pygame.Rect(x*scale, y*scale, scale, scale))
                # draw a line from the centre of this cell, to the centre of the cell stored in the value of "C"
                #print(c)
                #pygame.draw.line(WINDOW, (255,0,0), (x*scale+hScale, y*scale+hScale), (c[1]*scale+hScale, c[0]*scale+hScale))
                pygame.draw.line(WINDOW, (255,0,0), (x*scale, y*scale), (c[1]*scale, c[0]*scale))

    for cl in map.currentCandidateList:
        for c in cl:
            pygame.draw.rect(WINDOW, (255,255,0), pygame.Rect(c[1]*scale, c[0]*scale, scale, scale))


    if done and runOnce:
        # TODO - I think there is some bugs with the drawing here, as it goes diagonal across blocks some times. I'm taking it on faith
        # that CW got the co-ords right as well. (tbf - they do look consistent with above)
        sPath=map.getShortestPathToTarget()
        for c in sPath:
            print(c)

        runOnce=False

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