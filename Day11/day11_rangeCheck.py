from enum import Enum

def printStar(s):
    # unpairedStars.append({"display":map[i][j], "paired":False, "partner":None, "location":(i,j), "number":starNum})
    print(s["starNum"],end=" | ")
    print(s["partner"])

def checkForPairInRange(uList, star, r):
    x=star["location"][0]
    y=star["location"][1]
    rows=r
    
    # Test cardinals
    testx=x+rows
    testy=y
    print(str(testx)+","+str(testy),end="|")
    u=checkForPairAtLocation(uList,testx,testy)
    if u!=None:
        return u

    testx=x-rows
    testy=y
    print(str(testx)+","+str(testy),end="|")
    u=checkForPairAtLocation(uList,testx,testy)
    if u!=None:
        return u

    testx=x
    testy=y+rows
    print(str(testx)+","+str(testy),end="|")
    u=checkForPairAtLocation(uList,testx,testy)
    if u!=None:
        return u

    testx=x
    testy=y-rows
    print(str(testx)+","+str(testy),end="|")
    u=checkForPairAtLocation(uList,testx,testy)
    if u!=None:
        return u
    
    i=0
    while rows>0:
        # test diagonals - diagonals are 1 closer than the cardinals
        rows-=1
        i+=1
        if rows==0:
            print()
            break

        testx=x+rows
        testy=y+i
        print(str(testx)+","+str(testy),end="|")
        u=checkForPairAtLocation(uList,testx,testy)
        if u!=None:
            return u

        testx=x-rows
        testy=y+i
        print(str(testx)+","+str(testy),end="|")
        u=checkForPairAtLocation(uList,testx,testy)
        if u!=None:
            return u
        
        testx=x+rows
        testy=y-i
        print(str(testx)+","+str(testy),end="|")
        u=checkForPairAtLocation(uList,testx,testy)
        if u!=None:
            return u

        testx=x-rows
        testy=y-i
        print(str(testx)+","+str(testy),end="|")
        u=checkForPairAtLocation(uList,testx,testy)
        if u!=None:
            return u

        print()



def checkForPairAtLocation(uList,x,y):
    for u in uList:
        if u["paired"]==False:
            if u["location"][0]==x and u["location"][1]==y:
                #uList.remove(u)
                return u
    
    return None


# load a text file
# read file input.txt into an array of strings
file1 = open('Day11/data/input_test.txt', 'r')
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
            starList.append({"display":map[i][j], "paired":False, "partner":None, "location":(i,j), "starNum":starNum})
            starNum+=1

print(starList)
print("**** PAIRING STARS")


# lets check each unpaired star for a partner
range=1
while len(starList)>0 and range<20: 
    print("** Checking unpaired stars for range:"+str(range))
    for currentStar in starList:

        # Skip this star if its already paired, to stop us overwriting it
        if currentStar["paired"]==True:
            continue

        print("** Looking for pair for: ",end="")
        print(currentStar["location"])
        # code to check for pairs, moving paired stars out of the list
        # any unpaired stars we then check for a bigger radius and repeat until we've
        # found all the stars partners
        p=checkForPairInRange(starList,currentStar,range)

        if p!=None:
            p["paired"]=True
            p["partner"]=currentStar["starNum"]
            currentStar["paired"]=True
            currentStar["partner"]=p["starNum"]

            print("Found a pair: ",end="")
            print(p["location"],end=" with ")
            print(currentStar["location"])
            break
        #break

    range+=1

print("****  STARS")
for p in starList:
    printStar(p)
