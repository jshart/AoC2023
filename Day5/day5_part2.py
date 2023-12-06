class Map:
    def __init__(self,name):
        self.name=name

        parts=name.split("-");

        self.source=parts[0]
        self.to=parts[2]

        #the destination range start, the source range start, and the range length.
        self.ranges=[]

    def splitRanges(self,inputRange):
        outputRange=[]
        mappedInput=[]
        unmappedInput=[]
        stillToProcess=[]

        # Add the input ange to the unmappedInput list
        stillToProcess.append(inputRange)

        for mapRange in self.ranges:
            for unprocessed in stillToProcess:
                print("----> Testing Range:"+str(mapRange[0])+" "+str(mapRange[1])+" "+str(mapRange[2]))
                sourceRange1=mapRange[1]
                sourceRange2=mapRange[1]+mapRange[2]
                destRange1=mapRange[0]
                destRange2=mapRange[0]+mapRange[2]
                delta=mapRange[0]-mapRange[1]

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
                    unprocessed[0]=unprocessed[0]+delta
                    unprocessed[1]=unprocessed[1]+delta
                    mappedInput.append([unprocessed[0],unprocessed[1]])
                    print("---> Complete overlap")
                elif startInsideRange:
                    # This means that the start is inside the source range,
                    # but the end is outside the sorce range. So we need
                    # to split the input range into two parts.

                    #left (start) half overlaps, so gets mapped to dest range
                    mappedInput.append([unprocessed[0]+delta,destRange2])

                    #right (end) half does not overlap, so gets "passed through"
                    unmappedInput.append([sourceRange2+1,unprocessed[1]])
                    print("---> Partial overlap: start")
                elif endInsideRange:
                    # This means that the end is inside the source range,
                    # but the start is outside the source range. So we need
                    # to split the input range into two parts.


                    #left (start) half does not overlap, so gets "passed through"
                    unmappedInput.append([unprocessed[0],sourceRange1-1])
                    
                    #right (end) half overlaps, so gets mapped to dest range
                    mappedInput.append([destRange1,unprocessed[1]+delta])
                    print("---> Partial overlap: end")

            if len(unmappedInput)>0:
                stillToProcess.clear()
                stillToProcess=unmappedInput.copy()
                unmappedInput.clear()

        return(mappedInput+stillToProcess)

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
file1 = open('Day5/data/input_test.txt', 'r')
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
        # to add it the current map object - TODO
        map.addRange(lines[c])

for m in maps:
    print("Map:",m)
    maps[m].printMap()

currentSeedRanges=[]
newListOfRanges=[]

print("---------------- END OF LOAD ---------------")
print("Starting Seeds:")
for s in startingSeeds:
    print(s)

for s in startingSeeds:
    print("---------------- START OF RUN ---------------")
    print("Processing Seed Range:",s)
    newListOfRanges.clear()

    currentSeedRanges.clear()
    currentSeedRanges.append(s)

    tabPointer="seed"
    endPointer="location"
    searching=True

    while tabPointer != endPointer:

        fetchedMap=maps[tabPointer]
        print("--> Fetching:",tabPointer)

        for p in currentSeedRanges:
            print("--> Calling split with:",end="")
            print(p)

            newListOfRanges=fetchedMap.splitRanges(p)
            print("--> Returned processed ranges:")
            for a in newListOfRanges:
                print(a,end=" ")
            print()

        currentSeedRanges.clear()
        currentSeedRanges=newListOfRanges.copy()

        #move the pointer to the next map
        tabPointer=fetchedMap.to


    newListOfRanges.sort()
    print("Final Seeds:")
    print(newListOfRanges)