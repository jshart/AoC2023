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

def printMap(map):
    for r in map:
        print(r)
    print("****")


# TODO - I need to add the "cant travel in the same direction for more than 3 squares"
# limitation, as well as only allowing to go right/left/forward.
# Need some sort of direction history? Maybe backtrack along the trace matrix?
def searchPath(m,v):
    #print(candidates,end=" v:")
    #print(v)

    # find the lowest number candidate
    for hashCandidates in map.currentCandidateList:
        if len(hashCandidates)>0:
            candidate = hashCandidates.pop(0)
            break
    
    row=candidate[0] # rows (y)
    col=candidate[1] # columns (x)

    # West?
    if col>0 and col<len(m.trace[0])-1:
        if m.trace[row][col-1]==0:                              # Have we visited this cell before?
            m.trace[row][col-1]=candidate                       # if not, track the path to this cell
            newCandidate=[row,col-1]                            # create a new candidate list for this cell 
            v=m.map[row][col-1]                                 # get the weight from the map
            if newCandidate not in map.currentCandidateList[v]:   # is this candidate alread in the hashmap?
                map.currentCandidateList[v].append(newCandidate)  # it isn't so add it.

    # East?     
    if col>=0 and col<len(m.trace[0])-1:
        if m.trace[row][col+1]==0:
            m.trace[row][col+1]=candidate
            newCandidate=[row,col+1]
            v=m.map[row][col+1]
            if newCandidate not in map.currentCandidateList[v]:
                map.currentCandidateList[v].append(newCandidate)
    
    # North?
    if row>0 and row<len(m.trace)-1:
        if m.trace[row-1][col]==0:
            m.trace[row-1][col]=candidate
            newCandidate=[row-1,col]
            v=m.map[row-1][col]
            if newCandidate not in map.currentCandidateList[v]:
                map.currentCandidateList[v].append(newCandidate)

    # South?
    if row>=0 and row<len(m.trace)-1:
        if m.trace[row+1][col]==0:
            m.trace[row+1][col]=candidate
            newCandidate=[row+1,col]
            v=m.map[row+1][col]
            if newCandidate not in map.currentCandidateList[v]:
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
        self.map=[]
        self.trace=[]
        for c,l in enumerate(lines):
            lines[c]=lines[c].strip()
            tempMapLine=list(lines[c])
            for c,t in enumerate(tempMapLine):
                tempMapLine[c]=int(t)
            self.map.append(tempMapLine)
            self.trace.append([0] * len(tempMapLine))

        #self.printMap("Map Init")

        self.targetRow=len(self.map)
        self.targetCol=len(self.map[0])

        # Treat currentCandidateList as a hashmap - we create a seperate list
        # for each candidate who has a cost score 1-9
        self.currentCandidateList=c=[[] for x in range(10)]

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
                print(self.trace[r][c],end="|")
            print()

    def printShortestPathToTarget(self):
        cost=0
        tRow=len(map.trace)-1
        tCol=len(map.trace[0])-1
        cost+=map.map[tRow][tCol]

        while tRow>0 or tCol>0:
            print(map.trace[tRow][tCol],end=" ")
            tRow=map.trace[tRow][tCol][0]
            tCol=map.trace[tRow][tCol][1]
            cost+=map.map[tRow][tCol]
        print(" Cost="+str(cost))

    def getShortestPathToTarget(self):
        result=[]
        tRow=len(map.trace)-1
        tCol=len(map.trace[0])-1
        while tRow>0 or tCol>0:
            tRow=map.trace[tRow][tCol][0]
            tCol=map.trace[tRow][tCol][1]
            result.append(map.trace[tRow][tCol])
        return(result)


map=Map(lines)
map.printMap("Initial State")
print("**** DATA LOAD COMPLETE, starting run")

print("valid paths test:")
map.currentCandidateList[map.map[0][0]].append([0,0])
s=0
maxSteps=100

#for s in range(maxSteps):
done=False
while not done:
    s+=1
    searchPath(map,s)
    #map.printTrace("Search Path test")

    done=True
    for c in map.currentCandidateList:
        if len(c)>0:
            done=False
            break


print("**** RUN COMPLETE, final state is:")
total=0

print("Total is: "+str(total))

#map.printShortestPathToTarget()

import pygame, sys, random
from pygame.locals import *
pygame.init()

# Colours
BACKGROUND = (255, 255, 255)
 
# Game Setup
FPS = 60
if testing:
    scale=10
else:
    scale=5
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = map.targetCol*scale
WINDOW_HEIGHT = map.targetRow*scale
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AoC Display')


# Render elements of the game
WINDOW.fill(BACKGROUND)

printOnce=True
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
    
    # Main draw loop
    for y,l in enumerate(map.trace):
        for x,c in enumerate(l):
            # if c==1:
            #     #pygame.draw.rect(WINDOW, color, pygame.Rect((x*scale)-1, (y*scale)-1, scale-1, scale-1))
            #     pygame.draw.rect(WINDOW, red, pygame.Rect(x*scale, y*scale, scale, scale))
            # elif c==2:
            #     pygame.draw.rect(WINDOW, green, pygame.Rect(x*scale, y*scale, scale, scale))
            # elif c==3:
            #     pygame.draw.rect(WINDOW, blue, pygame.Rect(x*scale, y*scale, scale, scale))

            #pygame.draw.rect(WINDOW, (math.floor(255/(c[0]+1)),0,0), pygame.Rect(x*scale, y*scale, scale, scale))
            # draw a line from the centre of this cell, to the centre of the cell stored in the value of "C"
            if c!=0:
                #print(c)
                pygame.draw.line(WINDOW, (255,0,0), (x*scale+scale/2, y*scale+scale/2), (c[1]*scale+scale/2, c[0]*scale+scale/2))


    # TODO - I think there is some bugs with the drawing here, as it goes diagonal across blocks some times. I'm taking it on faith
    # that CW got the co-ords right as well. (tbf - they do look consistent with above)
    sPath=map.getShortestPathToTarget()
    oldC=sPath[0]
    for c in sPath:
        if printOnce:
            print(c)
        # draw a line from centre of current cell, to the centre of the cell stored in the value of "C"
        pygame.draw.line(WINDOW, (0,0,255), (oldC[1]*scale+scale/2, oldC[0]*scale+scale/2), (c[1]*scale+scale/2, c[0]*scale+scale/2))
        oldC=c

    printOnce=False

    #pygame.display.flip()

    pygame.display.update()
    fpsClock.tick(FPS)