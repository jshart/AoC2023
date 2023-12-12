from enum import Enum

def mDist(s,d,exRows,exCols):
    sx=s[1]
    sy=s[0]
    dx=d[1]
    dy=d[0]

    expansionFactor=1000000

    # Now that we're ready to calculate  the *pre-expansion* mDist, we need to
    # check to see if the path between this pair crosses an expansion
    # line, if it does we need to the remember how much extra we need to add
    # on to the mDist

    extraCols=0
    if sx>dx:
        xdelta=sx-dx
        for i in range(dx,sx):
            if i in exCols:
                extraCols+=1
                print("c"+str(i),end=",")
    else:
        xdelta=dx-sx
        for i in range(sx,dx):
            if i in exCols:
                extraCols+=1
                print("c"+str(i),end=",")

    xdelta-=extraCols
    xdelta=xdelta+(extraCols*expansionFactor)

    extraRows=0
    if sy>dy:
        ydelta=sy-dy
        for i in range(dy,sy):
            if i in exRows:
                extraRows+=1
                print("r"+str(i),end=",")

    else:
        ydelta=dy-sy
        for i in range(sy,dy):
            if i in exRows:
                extraRows+=1
                print("r"+str(i),end=",")

    ydelta-=extraRows
    ydelta=ydelta+(extraRows*expansionFactor)

    total=xdelta+ydelta
    print()
    return (total,extraCols,extraRows)

# load a text file
# read file input.txt into an array of strings
file1 = open('Day11/data/input.txt', 'r')
lines = file1.readlines()

def printMap(lines,msg):
    print("**** "+msg)
    for c,l in enumerate(lines):
        temp="".join(l)
        temp+=" ["+str(c)+"]"
        #temp2=temp.replace("."," ")
        print(temp)

map=[]
# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    tempMap=list(lines[c])
    map.append(tempMap)

printMap(map,"START STATE")

# FOR PART 2 - TODO - rework the expansion code, so that instead of actually
# expanding the grid, we track which rows/cols are empty, and then every time
# we cross one of those we need to increase the mDist by the expansion factor

# Lets do the space expansion. First of all lets check all the columns
# for any columns which are completely empty. If find any we need to 
# duplicate them. We do this search backwards so that we dont mess
# up the indexing when we insert a column
emptyColList=[]
for i in range(len(map[0])-1,-1,-1):

    # drop down this column. If we find anything other than a "."
    # then this column is not empty
    emptyCol=True
    for j in range(0,len(map)):
        if map[j][i]!=".":
            emptyCol=False
            break

    if emptyCol==True:
        # Empty col found
        print("Empty at column:"+str(i))
        emptyColList.append(i)

printMap(map,"AFTER SPACE EXPANSION HOR")

# Lets do the space expansion, part 2 - now we need to go row
# by row and check if any rows are completely empty. If find any
# we need to duplicate them.
# Ww do this loop backwards so that we dont mess up the indexing
emptyRowList=[]
for i in range(len(map)-1,-1,-1):

    # drop down this row. If we find anything other than a "."
    # then this row is not 
    emptyRow=True
    for j in range(0,len(map[0])):
        if map[i][j]!=".":
            emptyRow=False
            break

    if emptyRow==True:
        # Empty row found
        print("Empty at row:"+str(i))
        emptyRowList.append(i)
        
printMap(map,"AFTER SPACE EXPANSION VER")
print("Empty Cols:",end="")
print(emptyColList)
print("Empty Rows:",end="")
print(emptyRowList)

# Space is expanded, now we need to process the space looking for star pairs.
# We need to iteratively look for pairs that are further apart, so we start
# with looking for stars directly adjacent to each other, then one part,
# then two apart etc

# This is manhatten distance apart, so we dont consider diagonals, except
# in so much as they are "2 apart", i.e. one step to the side, one step up/down
# Effectively we need to search an ever increasing "Diamond" shape from our star
# out until we've found an unmatched star

# lets create 2 lists, one for the paired stars and one for the unmatched stars
starList=[]
starNum=1
for i in range(0,len(map)):
    for j in range(0,len(map[0])):
        # is this a star?
        if map[i][j]=="#":
            starList.append([i,j,starNum])
            starNum+=1

print(starList)

# we now need to check the mDist for every pair of stars in starList
i=0
c=len(starList)
total=0
# loop backwards through the list so that we dont mess up the indexing
# when we prune the one that we've just completed
for j in range(c-1,-1,-1):
    s=starList[j]
    for d in starList:
        if s!=d:
            i+=1
            md=mDist(s,d,emptyRowList,emptyColList)
            # co-ords are in row/col format
            print(str(i)+" -> "+str(s)+" to "+str(d)+" = "+str(md))
            total+=md[0]

    starList.remove(s)


print("Total = "+str(total))

# 840989451783 - off by 10?