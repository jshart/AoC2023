# https://www.redblobgames.com/pathfinding/a-star/introduction.html

from enum import Enum
import math
testing=False

# create an enum for the compass cardinal directions
class WallState(Enum):
    Outside=0
    Onwall=1
    Inside=2

def printMap(map):
    for r in map:
        print(r)
    print("****")


def floodFill(m,candidates,v):
    #print(candidates)
    c = candidates.pop(0)
    x=c[0] # columns
    y=c[1] # rows
    if m[y][x]==0:
        m[y][x]=v

    if x>0 and x<len(m[0])-1:
        if m[y][x-1]==0:
            newC=[x-1,y]
            if newC not in candidates:
                candidates.append(newC)
        if m[y][x+1]==0:
            newC=[x+1,y]
            if newC not in candidates:
                candidates.append(newC)
    
    if y>0 and y<len(m)-1:
        if m[y-1][x]==0:
            newC=[x,y-1]
            if newC not in candidates:
                candidates.append(newC)
        if m[y+1][x]==0:
            newC=[x,y+1]
            if newC not in candidates:
                candidates.append(newC)
            


def floodFillRecursive(m,x,y,v,d):
    # starting at x,y, flood fill until we hit a wall or the edge of the map
    map[y][x]=v

    insideX=False
    insideY=False
    if d>990:
        return
    if x>0 and x<len(m[0])-1:
        if map[y][x-1]==0:
            floodFillRecursive(m,x-1,y,v,d+1)
        if map[y][x+1]==0:
            floodFillRecursive(m,x+1,y,v,d+1)

        insideX=True
    
    if y>0 and y<len(m)-1:
        if map[y-1][x]==0:
            floodFillRecursive(m,x,y-1,v,d+1)
        if map[y+1][x]==0:
            floodFillRecursive(m,x,y+1,v,d+1)

        insideY=True

    if insideX and insideY:
        # Do the 4 corners as well
        if map[y-1][x-1]==0:
            floodFillRecursive(m,x-1,y-1,v,d+1)
        if map[y-1][x+1]==0:
            floodFillRecursive(m,x+1,y-1,v,d+1)
        if map[y+1][x-1]==0:
            floodFillRecursive(m,x-1,y+1,v,d+1)
        if map[y+1][x+1]==0:
            floodFillRecursive(m,x+1,y+1,v,d+1)


# load a text file
# read file input.txt into an array of strings
if testing:
    file1 = open('Day18/data/input_test.txt', 'r')
    lines = file1.readlines()
else:
    file1 = open('Day18/data/input.txt', 'r')
    lines = file1.readlines()

# Lets work out our boundary, lets start by counting up all the right/down
# moves as that'll give us an absolute max size.

# maxRows=0
# maxCols=0
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    parts=lines[c].split(" ")

    # if parts[0] == "D":
    #     maxRows+=int(parts[1])
    # if parts[0] == "R":
    #     maxCols+=int(parts[1])

    lines[c]=parts.copy()

# Lets add some buffer to make debugging the space easier
#High/low Row: 223/-235
#High/low Col: 388/-53

if testing:
    maxRows=20
    maxCols=20
else:
    maxRows=223+235+1
    maxCols=388+53+1


print("Max Rows: "+str(maxRows))
print("Max Cols: "+str(maxCols))

# Lets make a 2 dimensional array size of maxRows, maxCols
# and set all the elements to zero
map = [[0 for x in range(maxCols)] for y in range(maxRows)]


# Offset these to remove the negative part of the map
if testing:
    sr=0
    sc=0
else:
    sr=235
    sc=53

highr=0
lowr=0
highc=0
lowc=0
for c,l in enumerate(lines):
    print("-> Line = ",end="")
    print(lines[c])

    # EXPERIMENT - scale down the whole image
    # lines[c][1]=str(math.ceil(int(lines[c][1])/10))
    # print(lines[c][1])

    if lines[c][0]=='U':
        for i in range(int(lines[c][1])):
            sr-=1
            print("sr: "+str(sr)+" sc: "+str(sc))
            map[sr][sc]=1
    elif lines[c][0]=='D':
        for i in range(int(lines[c][1])):
            sr+=1
            map[sr][sc]=1
    elif lines[c][0]=='L':
        for i in range(int(lines[c][1])):
            sc-=1
            map[sr][sc]=1
    elif lines[c][0]=='R':
        for i in range(int(lines[c][1])):
            sc+=1
            map[sr][sc]=1

    if sr>highr:
        highr=sr
    if sc>highc:
        highc=sc
    if sr<lowr:
        lowr=sr
    if sc<lowc:
        lowc=sc

print("High/low Row: "+str(highr)+"/"+str(lowr))
print("High/low Col: "+str(highc)+"/"+str(lowc))
print("**** DATA LOAD COMPLETE, starting run")
#printMap(map)

print("filling in the inside")
midR=(highr+lowr)//2
midC=(highc+lowc)//2
#map[midR][midC]=2

candidateList=[[midC,midR]]
while len(candidateList)>0:
    floodFill(map,candidateList,2)
#floodFillRecursive(map,midC,midR,2,0)

wallCount=0
insideCount=0
for r in map:
    for c in r:
        if c==1:
            wallCount+=1
        elif c==2:
            insideCount+=1

# Print out the results and the total
print("Walls: "+str(wallCount))
print("Inside: "+str(insideCount))
print("Total: "+str(wallCount+insideCount))

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
    scale=1
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = maxCols*scale
WINDOW_HEIGHT = maxRows*scale
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AoC Display')


# Render elements of the game
WINDOW.fill(BACKGROUND)

looping=True
 # The main game loop
while looping:
    # Get inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Initializing Color
    wallColour = (255,0,0)
    insideColour= (0,255,0)
    
    # Main draw loop
    for y,l in enumerate(map):
        for x,c in enumerate(l):
            if c==1:
                #pygame.draw.rect(WINDOW, color, pygame.Rect((x*scale)-1, (y*scale)-1, scale-1, scale-1))
                pygame.draw.rect(WINDOW, wallColour, pygame.Rect(x*scale, y*scale, scale, scale))
            elif c==2:
                pygame.draw.rect(WINDOW, insideColour, pygame.Rect(x*scale, y*scale, scale, scale))
    
    #pygame.display.flip()

    pygame.display.update()
    fpsClock.tick(FPS)