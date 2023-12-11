from enum import Enum

def mDist(s,d):
    sx=s[0]
    sy=s[1]
    dx=d[0]
    dy=d[1]

    if sx>dx:
        xdelta=sx-dx
    else:
        xdelta=dx-sx

    if sy>dy:
        ydelta=sy-dy
    else:
        ydelta=dy-sy

    total=xdelta+ydelta
    return total

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

# Lets do the space expansion. First of all lets check all the columns
# for any columns which are completely empty. If find any we need to 
# duplicate them. We do this search backwards so that we dont mess
# up the indexing when we insert a column
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
        print("Expanding at column:"+str(i))
        for j in range(0,len(map)):
            map[j].insert(i,".")

printMap(map,"AFTER SPACE EXPANSION HOR")

# Lets do the space expansion, part 2 - now we need to go row
# by row and check if any rows are completely empty. If find any
# we need to duplicate them.
# Ww do this loop backwards so that we dont mess up the indexing
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
        print("Expanding at row:"+str(i))
        map.insert(i,list("."*len(map[0])))
        
printMap(map,"AFTER SPACE EXPANSION VER")

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
for j in range(c-1,-1,-1):
    s=starList[j]
    for d in starList:
        if s!=d:
            i+=1
            md=mDist(s,d)
            print(str(i)+" -> "+str(s)+" to "+str(d)+" = "+str(md))
            total+=md
    starList.remove(s)


print("Total = "+str(total))