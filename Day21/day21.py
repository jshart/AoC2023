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


class Cell(Enum):
    Empty=0
    Rock=1
    Start=2
    Step=3

# load a text file
# read file input.txt into an array of strings
if testing:
    file1 = open('Day21/data/input_test.txt', 'r')
    lines = file1.readlines()
else:
    file1 = open('Day21/data/input.txt', 'r')
    lines = file1.readlines()

class Map:
    def __init__(self,lines):
        self.drawMap=[]
        self.scratchMap=[]
        for c,l in enumerate(lines):
            lines[c]=lines[c].strip()
            tempMapLine=list(lines[c])
            for c,t in enumerate(tempMapLine):
                if t==".":
                    tempMapLine[c]=Cell.Empty
                elif t=="#":
                    tempMapLine[c]=Cell.Rock
                elif t=="S":
                    tempMapLine[c]=Cell.Step
            self.drawMap.append(tempMapLine)
            self.scratchMap.append([Cell.Empty] * len(tempMapLine))

        self.maxRow=len(self.drawMap)
        self.maxCol=len(self.drawMap[0])

        # self.neighbours=[(-1,-1),(0,-1),(+1,-1),
        #                  (-1,0),        (+1,0),
        #                  (-1,+1),(0,+1),(+1,+1)]
        self.neighbours=[(0,-1),
                         (-1,0),        (+1,0),
                         (0,+1)]
        
    
    def updateMap(self):
        stepCount=0
        # check each element in the map?
        for r in range(len(self.drawMap)):
            for c in range(len(self.drawMap[r])):

                # is this a previous step space?
                if self.drawMap[r][c]==Cell.Step:
                    # if we offset this by the neighbour co-ords is there an empty space?
                    for n in self.neighbours:
                        # is this in range of the grid?
                        if r+n[0]>=0 and r+n[0]<self.maxRow and c+n[1]>=0 and c+n[1]<self.maxCol:
                            # is this an empty space?
                            if self.drawMap[r+n[0]][c+n[1]]==Cell.Empty and self.scratchMap[r+n[0]][c+n[1]]==Cell.Empty:
                                self.scratchMap[r+n[0]][c+n[1]]=Cell.Step
                                stepCount+=1
                elif self.drawMap[r][c]==Cell.Rock:
                    self.scratchMap[r][c]=Cell.Rock
        print("Steps for this update: "+str(stepCount))

    def flipMap(self):
        for r in range(len(self.drawMap)):
            for c in range(len(self.drawMap[r])):
                self.drawMap[r][c]=self.scratchMap[r][c]
                self.scratchMap[r][c]=Cell.Empty


    def printMap(self,s):
        print("** "+s+" **")
        for r in range(len(self.drawMap)):
            for c in range(len(self.drawMap[r])):
                print(self.drawMap[r][c],end="")
            print()




map=Map(lines)
map.printMap("Initial State")
print("**** DATA LOAD COMPLETE, starting run")

s=0
maxSteps=64


import pygame, sys, random
from pygame.locals import *
pygame.init()

# Colours
# Initializing Color
red = (255,0,0)
green= (0,255,0)
blue= (0,0,255)
grey= (128,128,128)
yellow = (255,255,0)
brown = (128,64,0)
BACKGROUND = green
 
# Game Setup
FPS = 60
if testing:
    scale=10
else:
    scale=5

hScale=math.ceil(scale/2)

fpsClock = pygame.time.Clock()
WINDOW_WIDTH = map.maxCol*scale
WINDOW_HEIGHT = map.maxRow*scale
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AoC Display')

 # The main game loop
while True:
    # Render elements of the game
    WINDOW.fill(BACKGROUND)

    # Get inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Main draw loop
    for y,l in enumerate(map.drawMap):
        for x,c in enumerate(l):

            if c==Cell.Rock:
                pygame.draw.rect(WINDOW, grey, pygame.Rect(x*scale, y*scale, scale, scale))
            elif c==Cell.Step:
                pygame.draw.rect(WINDOW, brown, pygame.Rect(x*scale, y*scale, scale, scale))
            elif c==Cell.Start:
                pygame.draw.rect(WINDOW, red, pygame.Rect(x*scale, y*scale, scale, scale))

    if s<1:
        # Wait 5 seconds before starting animation
        pygame.display.update()
        pygame.time.wait(5000)


    if s<maxSteps:
        pygame.time.wait(500)
        print("Updating")
        map.updateMap()
        print("Flipping")
        map.flipMap()
        s+=1
        print("Step "+str(s))

    pygame.display.update()
    fpsClock.tick(FPS)