class Map:
    def __init__(self,name):
        self.name=name

        parts=name.split("-");

        self.source=parts[0]
        self.to=parts[2]

        self.ranges=[]

    def printMap(self):
        print("Map: ",self.name)
        print("Source:",self.source)
        print("To:",self.to)
        for r in self.ranges:
            print(r)

    def addRange(self,rangeString):
        newRange=[]
        parts=rangeString.split(" ")
        for p in parts:
            newRange.append(int(p))
        self.ranges.append(newRange)


# load a text file
# read file input.txt into an array of strings
file1 = open('Day5/data/input.txt', 'r')
lines = file1.readlines()

maps={}

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
        print(parts)
    elif parts[1]=="map:":
        print("Map:",end="")
        print(parts)

        # create a new map object and add it to the map list
        # the parts[0] here just contains the name, as the "map" text
        # at the end has already been stripped. The class contructor
        # will divide up the rest
        map=Map(parts[0])
        maps[parts[0]] = map
    else:
        # otherwise this line should be a map content part, and we need
        # to add it the current map object - TODO
        map.addRange(lines[c])

for m in maps:
    maps[m].printMap()

