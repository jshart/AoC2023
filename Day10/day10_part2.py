from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day10/data/input.txt', 'r')
lines = file1.readlines()

# Here are the types of pipe connections
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

def connectsTo(c):
    retval=""

    #print("C2:"+c,end=" ")
    if c=="|":
        retval = "NS"
    elif c=="-":
        retval = "EW"
    elif c=="L":
        retval = "NE"
    elif c=="J":
        retval = "NW"
    elif c=="F":
        retval = "SE"
    elif c=="7":
        retval = "SW"
    elif c=="S":
        retval = "NESW"
    
    #print("Ret:"+retval)

    return retval

def connectForward(c,direction):
    validConnection=False

    if c=="|":
        if direction=="N" or direction=="S":
            validConnection=True
    elif c=="-":
        if direction=="E" or direction=="W":
            validConnection=True
    elif c=="L":
        if direction=="N" or direction=="E":
            validConnection=True
    elif c=="J":
        if direction=="N" or direction=="W":
            validConnection=True
    elif c=="F":
        if direction=="S" or direction=="E":
            validConnection=True
    elif c=="7":
        if direction=="S" or direction=="W":
            validConnection=True
    elif c=="S":
        validConnection=True
    
    return validConnection

def connectBackward(c,direction):
    validConnection=False

    if c=="|":
        if direction=="N" or direction=="S":
            validConnection=True
    elif c=="-":
        if direction=="E" or direction=="W":
            validConnection=True
    elif c=="L":
        if direction=="N" or direction=="E":
            validConnection=True
    elif c=="J":
        if direction=="N" or direction=="W":
            validConnection=True
    elif c=="F":
        if direction=="S" or direction=="E":
            validConnection=True
    elif c=="7":
        if direction=="S" or direction=="W":
            validConnection=True
    elif c=="S":
        validConnection=True
    
    return validConnection


def printMap(lines,msg):
    print("**** "+msg)
    for l in lines:
        temp="".join(l)
        temp2=temp.replace("."," ")
        print(temp2)

map=[]
# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMap=list(lines[c])
    map.append(tempMap)

printMap(map,"START STATE")

maxLoops=100
done=False
while not done and maxLoops>0:
    done=True
    maxLoops-=1

    for y,l in enumerate(map):
        for x,c in enumerate(l):
            # keep track of the start location once we find it
            if c=="S":
                startX=x
                startY=y

            # which cells do we need to check for a valid
            # pipe connection based on this type?
            # This returns *All* of the connectinons that
            # need to met
            allowedDirections=connectsTo(c)

            # Build a matrix for what directions are valid and correct
            matrix={}
            for d in allowedDirections:
                matrix[d]=False

            # Based on the possible directions, lets check *EACH* if both sides of the
            # pipe see this as a legit connection
            if "N" in allowedDirections and y>0:
                if connectForward(map[y][x],"N") and connectBackward(map[y-1][x],"S"):
                    matrix["N"]=True
            if "S" in allowedDirections and y<len(lines)-1:
                if connectForward(map[y][x],"S") and connectBackward(map[y+1][x],"N"):
                    matrix["S"]=True
            if "E" in allowedDirections and x<len(l)-1:
                if connectForward(map[y][x],"E") and connectBackward(map[y][x+1],"W"):
                    matrix["E"]=True
            if "W" in allowedDirections and x>0:
                if connectForward(map[y][x],"W") and connectBackward(map[y][x-1],"E"):
                    matrix["W"]=True

            goodConnection=True
            for m in matrix:
                if matrix[m]==False:
                    goodConnection=False
                    break

            # If this is a bad connetion and its not already a blank space, lets
            # reset it. We also treat S as an always valid space.
            if map[y][x]!="." and map[y][x]!="S":
                if not goodConnection:
                    map[y][x]="."
                    done=False

    printMap(map,"END STATE")

print("**** Pruning complete, start location at:"+str(startX)+","+str(startY))

# S exists somewhere on the loop, but we dont know exactly what shape of pipe
# exists at this location. However because we pruned all the rest of the map of
# dead end pipes that are not part of a loop we can infer the shape of the pipe
# based on the fact there must be exact 2 legal adjacent pipe locations.

checkXStart = startX-1 if startX>0 else startX
checkXEnd = startX+1 if startX<len(l)-1 else startX
checkYStart = startY-1 if startY>0 else startY
checkYEnd = startY+1 if startY<len(lines)-1 else startY

print("**** Checking for pipes in range:"+str(checkXStart)+","+str(checkYStart)+" to "+str(checkXEnd)+","+str(checkYEnd))
print("**** Lines:"+str(len(lines))+" Columns:"+str(len(l)))

path=[]
possiblePaths=[]

# Lets check each of the cardinal points in turn and see which
# ones have a legal pipe direction to this location.
if startY>0:
    # we are able to check the pipe to the North - does it have a south connection?
    if connectBackward(map[startY-1][startX],"S"):
        print("Start can go North")
        possiblePaths.append([startY-1,startX,"S"])

if startY<len(lines)-1:
    # we are able to check the pipe to the South - does it have a north connection?
    if connectForward(map[startY+1][startX],"N"):
        print("Start can go South")
        possiblePaths.append([startY+1,startX,"N"])

if startX>0:
    # we are able to check the pipe to the West - does it have a east connection?
    if connectBackward(map[startY][startX-1],"E"):
        print("Start can go West")
        possiblePaths.append([startY,startX-1,"E"])

if startX<len(l)-1:
    # we are able to check the pipe to the East - does it have a west connection?
    if connectForward(map[startY][startX+1],"W"):
        print("Start can go East")
        possiblePaths.append([startY,startX+1,"W"])

print(possiblePaths)

# OK we've identified some possible paths to the end of the loop.
# lets just pick the first one and head off until we come back.
# Path format is y (row), x (column), direction we enter the next node from
# i.e. if we head north, we record south as we've *Consumed* the south path
# of the next node, which means we should exclude it from our selection
path.append([startY,startX,"S"])
path.append(possiblePaths[0])
done=False
while not done:
    # Where are we in the loop?
    p=path[-1]

    if p[0]==path[0][0] and p[1]==path[0][1]:
        steps=(len(path)-1)/2
        print("Loop completed with:"+str(steps)+" steps")
        done=True
    else:
        #print("Checking path["+map[p[0]][p[1]]+"]")

        # where can we go from here?
        directions=connectsTo(map[p[0]][p[1]])

        # remove the direction we came from from the list of possible 
        directions=directions.replace(p[2],"")

        # we only have one valid direction we can now travel in
        # lets fetch the next node;
        if directions=="N":
            path.append([p[0]-1,p[1],"S"])
        elif directions=="S":
            path.append([p[0]+1,p[1],"N"])
        elif directions=="E":
            path.append([p[0],p[1]+1,"W"])
        elif directions=="W":
            path.append([p[0],p[1]-1,"E"])

# Lets "highligt" the path so we can see it better
# for p in path:
#     map[p[0]][p[1]]="#"

printMap(map,"LOOP PATH")

# print("**** Checking X for range:"+str(checkXStart)+" to "+str(checkXEnd+1))
# for i in range(checkXStart,checkXEnd+1):
#     print("+-- Checking for pipe at:"+str(i)+","+str(startY))
#     if map[startY][i]!="S":
#         if map[startY][i]!=".":
#             print("  + Found a pipe at:"+str(i)+","+str(startY)+"= "+map[startY][i])

# print("**** Checking Y")
# for j in range(checkYStart,checkYEnd+1):
#     print("+-- Checking for pipe at:"+str(startX)+","+str(j))
#     if map[j][startX]!="S":
#         if map[j][startX]!=".":
#             print("  + Found a pipe at:"+str(startX)+","+str(j)+"= "+map[j][startX])


import pygame, sys, random
from pygame.locals import *
pygame.init()

# Colours
BACKGROUND = (255, 255, 255)
 
# Game Setup
FPS = 60
scale=5
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 140*scale
WINDOW_HEIGHT = 140*scale
 
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

    # Processing
    # This section will be built out later

        # Initializing Color
    color = (255,0,0)
    
    # Drawing Rectangle

    #TODO replace this with a map draw!
    for y,l in enumerate(map):
        for x,c in enumerate(l):
            if c!=".":
                #pygame.draw.rect(WINDOW, color, pygame.Rect((x*scale)-1, (y*scale)-1, scale-1, scale-1))

                if c=="|":
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)
                    ex=(x*scale)+(scale/2)
                    ey=(y*scale)+scale
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                elif c=="-":
                    sx=(x*scale)
                    sy=(y*scale)+(scale/2)
                    ex=(x*scale)+scale
                    ey=(y*scale)+(scale/2)
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    retval = "EW"
                elif c=="L":
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)
                    ex=(x*scale)+(scale/2)
                    ey=(y*scale)+(scale/2)
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)+(scale/2)
                    ex=(x*scale)+scale
                    ey=(y*scale)+(scale/2)
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    retval = "NE"
                elif c=="J":
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)
                    ex=(x*scale)+(scale/2)
                    ey=(y*scale)+(scale/2)
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)+(scale/2)
                    ex=(x*scale)
                    ey=(y*scale)+(scale/2)
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    retval = "NW"
                elif c=="F":
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)+(scale/2)
                    ex=(x*scale)+(scale/2)
                    ey=(y*scale)+scale
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)+(scale/2)
                    ex=(x*scale)+scale
                    ey=(y*scale)+(scale/2)
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    retval = "SE"
                elif c=="7":
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)+(scale/2)
                    ex=(x*scale)+(scale/2)
                    ey=(y*scale)+scale
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    sx=(x*scale)+(scale/2)
                    sy=(y*scale)+(scale/2)
                    ex=(x*scale)
                    ey=(y*scale)+(scale/2)
                    pygame.draw.line(WINDOW, (0,0,0), (sx, sy), (ex, ey))
                    retval = "SW"
                elif c=="S":
                    retval = "NESW"
    
    #pygame.display.flip()

    pygame.display.update()
    fpsClock.tick(FPS)