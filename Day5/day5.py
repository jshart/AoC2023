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
seeds=[]

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
        for i in range(1,len(parts)):
            seeds.append(int(parts[i]))
        print(seeds)

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

results=[]
for seed in seeds:
    tabPointer="seed"
    endPointer="location"
    searching=True

    print("Processing: "+str(seed))
    while tabPointer != endPointer:

        fetchedMap=maps[tabPointer]
        print("--> Fetching:",tabPointer,end="")
        result=fetchedMap.mapRange(seed)

        print(" Result:",result)
        seed+=result

        #move the pointer to the next map
        tabPointer=fetchedMap.to

    print("Seed final location:",seed)
    results.append(seed)

results.sort()
print("Final Seeds:")
print(results)