from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day14/data/input.txt', 'r')
lines = file1.readlines()

map=[]


# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMapLine=list(lines[c])
    map.append(tempMapLine)
    print(map[-1])

print("**** DATA LOAD COMPLETE, starting run")

# starting at the end of the map, check each row
# in turn - looking for "0"'s, if the space in the
# row above is free, we then move the "0" up.
# Repeat through out the map
# Note we skip the last row (ot the top of the map)
# as there are no places for that to move
#for i in range(len(map)-1,0,-1):
somethingMoved=True
while somethingMoved:
    somethingMoved=False
    for i in range(1,len(map)):

        print("processing:[",end="")
        print(map[i],end="")
        print("] index="+str(i))
        # lets check each character in the row
        # looking for a rock we can move
        for j in range(0,len(map[i])):
            if map[i][j]=="O":
                # is the cell above empty?
                if map[i-1][j]==".":
                    # move the rock up
                    map[i-1][j]="O"
                    map[i][j]="."
                    somethingMoved=True

print("**** FINAL MAP ****")
for m in map:
    print(m)

totalScore=0
# Score the grid
for c,m in enumerate(map):
    # how many rocks are in this row?
    rocks=m.count("O")
    lineScore=rocks*(len(map)-c)
    print("Line "+str(c)+" has "+str(rocks)+" rocks, score="+str(lineScore))
    totalScore+=lineScore

# Print the final total score
print("Total Score = "+str(totalScore))