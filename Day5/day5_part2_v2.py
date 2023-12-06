class Map:
    def __init__(self,name):
        self.name=name

        parts=name.split("-");

        self.source=parts[0]
        self.to=parts[2]

        #the destination range start, the source range start, and the range length.
        self.ranges=[]

    def printMap(self):
        print("S.Map: ",self.name)
        print("S.Source:",self.source)
        print("S.To:",self.to)
        for r in self.ranges:
            print(r)

    def addRange(self,rangeString):
        newRange=[]
        parts=rangeString.split(" ")
        for p in parts:
            newRange.append(int(p))
        self.ranges.append(newRange)

    def checkSourceRange(self,seed):
        for r in self.ranges:
            if seed>=r[1] and seed<=(r[1]+r[2]):
                return True
        return False
    
    def mapRange(self,seed):
        for r in self.ranges:
            if seed>=r[1] and seed<=(r[1]+r[2]):
                # this is inside the range so we need to return a delta to adjust
                # the number by
                return (r[0]-r[1])
        return 0
    
    def checkDestinationRange(self,seed):
        for r in self.ranges:
            if seed>=r[0] and seed<=(r[0]+r[2]):
                return True
        return False

# load a text file
# read file input.txt into an array of strings
file1 = open('Day5/data/input.txt', 'r')
lines = file1.readlines()

maps={}
startingSeeds=[]

for c,line in enumerate(lines):
    lines[c]=lines[c].strip()

    # break out the line by spaces
    parts=lines[c].split(" ")

    if len(parts)<2:
        # ignore blank lines
        continue

    # right, lets work out what we're loading and how to store it
    # first of all lets check for the seed list;
    if parts[0]=="seeds:":
        print("Seed List:",end="")
        for i in range(1,len(parts),2):
            a=int(parts[i])
            b=int(parts[i+1])
            startingSeeds.append([a,a+b])
        print(startingSeeds)

    elif parts[1]=="map:":
        print("Map:",end="")
        print(parts)

        # create a new map object and add it to the map list
        # the parts[0] here just contains the name, as the "map" text
        # at the end has already been stripped. The class contructor
        # will divide up the rest
        map=Map(parts[0])
        maps[map.source] = map
    else:
        # otherwise this line should be a map content part, and we need
        # to add it the current map object
        map.addRange(lines[c])

for m in maps:
    print("Map:",m)
    maps[m].printMap()



print("---------------- END OF LOAD ---------------")
print("Starting Seeds:")
for s in startingSeeds:
    print(s)


currentSeedRanges=[]
mappedInput=[]
finalRun=[]

# Top level loop - loop through each of the seed pairs looking for the seed
# starting range that contains what we need.
for s in startingSeeds:
    print("---------------- START OF RUN ---------------")
    print("Processing Seed Range:",s)

    # Reset all the working list and flag data ready for this new run,
    # populate the currentSeedRanges list with just the base seed for the
    # start of this run
    currentSeedRanges.clear()
    currentSeedRanges.append(s)

    tabPointer="seed"
    endPointer="location"
    searching=True

    # Walk through each of the maps, checking the seed range against the entries
    # and determining if we need to chunk up the range etc
    while tabPointer != endPointer:

        fetchedMap=maps[tabPointer]
        print("o+-> Fetching:",tabPointer,end=" with input:")
        print(currentSeedRanges)


        # For a given table, our objective is to
        # 1) check the list of currentSeedRanges and any that match we move to a mappedInput
        #    list as they are translated.
        # 2) as we break and create subranges, any that fall outside of the dest range being
        #    checked, get recycled back into the currentSeedRanges list in case a later range
        #    in this table matches it.
        # 3) If we complete the range passes for the table and there are still ranges in the
        #    currentSeedRanges list, we need to treat them as "pass through" and simply
        #    include them "as is" for the next table pass
        # 4) once we have processed all the ranges in the currentSeedRanges list, we then
        #    are done with this pass, we need to move the mappedInput list into the currentSeedRanges
        #    ready for the next table

        # In the above example, the lowest location number can be obtained from seed number 82
        # which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46
        # and location 46. So, the lowest location number is 46.

        # loop through each of the ranges in this current map and lets check if the currentSeedRanges
        # match anything in here.
        for mapRange in fetchedMap.ranges:

            # Lets check each of the ranges in the currentSeedRanges list with this mapRange to see
            # if there is any overlap
            for i, unprocessed in enumerate(currentSeedRanges):
                print(" #--> Looking at if we need to split or map unprocessed range:",end="")
                print(unprocessed)
                if unprocessed==None:
                    print(" |--> None")
                    continue

                # Lets work out all the proper start/stop ranges for the source/dest
                print(" |--> Testing Table Range:"+str(mapRange[0])+" "+str(mapRange[1])+" "+str(mapRange[2]),end="")
                sourceRange1=mapRange[1]
                sourceRange2=mapRange[1]+mapRange[2]-1
                destRange1=mapRange[0]
                destRange2=mapRange[0]+mapRange[2]-1
                delta=mapRange[0]-mapRange[1]
                print(" Looking for source range match of:"+str(sourceRange1)+"->"+str(sourceRange2))

                startInsideRange=False
                endInsideRange=False

                # check if the input start is inside the source range
                if unprocessed[0]>=sourceRange1 and unprocessed[0]<=sourceRange2:
                    startInsideRange=True
                
                # check if the input end is inside the source range
                if unprocessed[1]>=sourceRange1 and unprocessed[1]<=sourceRange2:
                    endInsideRange=True
                    
                if startInsideRange and endInsideRange:
                    # Entire input is inside the source range
                    # so we just adjust the entire range by the delta
                    # we update this entry with the dest range (via the delta)
                    # and then we add it to the mappedInput as this is the list
                    # of stuff we've processed.
                    a=unprocessed[0]+delta
                    b=unprocessed[1]+delta
                    mappedInput.append([a,b])
                    print("  \--> Completely inside, remapped to:"+str(a)+"->"+str(b))

                    currentSeedRanges[i]=None
                elif startInsideRange:
                    # This means that the start is inside the source range,
                    # but the end is outside the sorce range. So we need
                    # to split the input range into two parts.
                    print("  \--> Partial overlap: start - addding:", end="")

                    #left (start) half overlaps, so gets mapped to dest range
                    a=unprocessed[0]+delta
                    b=destRange2
                    mappedInput.append([a,b])
                    print(mappedInput[-1],end=" ")

                    # right (end) half does not overlap, so gets added back to the stack
                    # to be processed again by any remaining ranges that it may match
                    a=sourceRange2+1
                    b=unprocessed[1]
                    currentSeedRanges.append([a,b])
                    print(currentSeedRanges[-1])
 

                    currentSeedRanges[i]=None
                elif endInsideRange:
                    # This means that the end is inside the source range,
                    # but the start is outside the source range. So we need
                    # to split the input range into two parts.
                    print("  \--> Partial overlap: end - adding:",end="")

                    # left (start) half does not overlap, so gets added back to the stack
                    # to be processed again by any remaining ranges that it may match
                    a=unprocessed[0]
                    b=sourceRange1-1
                    currentSeedRanges.append([a,b])
                    print(currentSeedRanges[-1],end=" ")

                    # right (end) half overlaps, so gets mapped to dest range
                    a=destRange1
                    b=unprocessed[1]+delta
                    mappedInput.append([a,b])
                    print(mappedInput[-1])
                    
                    currentSeedRanges[i]=None
                elif unprocessed[0]<sourceRange1 and unprocessed[1]>sourceRange2:
                    # this means the input range completely overlaps the source range
                    # so we need to break the input range into three parts, left (pass through),
                    # middle (mapped), right (pass through)
                    print("  \--> Complete overlap - adding:",end="")

                    a=unprocessed[0]
                    b=sourceRange1-1
                    currentSeedRanges.append([a,b])
                    print(currentSeedRanges[-1],end=" ")

                    a=destRange1
                    b=destRange2
                    mappedInput.append([a,b])
                    print(mappedInput[-1],end=" ")

                    a=sourceRange2+1
                    b=unprocessed[1]
                    currentSeedRanges.append([a,b])
                    print(currentSeedRanges[-1],end=" ")

                    currentSeedRanges[i]=None
            
            # END OF for unprocessed in currentSeedRanges:

        # END OF for mapRange in fetchedMap.ranges:

        # Once we've processed all the ranges in the current map, lets check 
        # if there are any ranges that did not match any of the ranges and are
        # still left in the currentSeedRanges list. If so, we need to add them
        # (unaltered) to the mappedInput as that is our list of stuff that has
        # been fully processed.
        if len(currentSeedRanges)>0:
            print(" |--> Checking unmapped ranges to see if any need adding to mappedInput for next pass:")
            #print(currentSeedRanges)
            #mappedInput.extend(currentSeedRanges)
            for c in currentSeedRanges:
                if c==None:
                    print(" \--> Item marked as None, skipping")
                    continue
                print(" \--> Adding to mappedInput:",end="")
                print(c,end="")
                mappedInput.append(c)
                print()

        # The mappedInput list now contains all the stuff we need to get ready
        # for the next table pass. Lets move the content across and reset the lists
        print(" |--> Resetting currentSeedRanges, adding:",end="")

        currentSeedRanges.clear()
        for m in mappedInput:
            print(m,end="")
            currentSeedRanges.append(m)
        mappedInput.clear()
        print()
   
        #move the pointer to the next map
        tabPointer=fetchedMap.to


    # END of while tabPointer != endPointer:
    print("Final currentSeedRanges for this run are:",end="")
    print(currentSeedRanges)
    print("Anything left in mappedInput:",end="")
    print(mappedInput)
    print("---------------- END OF RUN ---------------")

    for c in currentSeedRanges:
        finalRun.append(c)

finalRun.sort()
print("Final Run Results:",end="")
print(finalRun)