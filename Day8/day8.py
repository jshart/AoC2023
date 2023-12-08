from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day8/data/input.txt', 'r')
lines = file1.readlines()

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()

map={}

for l in lines:
    if "=" not in l:
        instructions=l
    else:
        parts=l.split("=")
        start=parts[0]
        parts2=parts[1].split(",")
        left=parts2[0]
        right=parts2[1]

        #print(start+" => "+left+" or "+right)

        map[start]=(left,right)

print(map)
print("**** Map loaded and formatted")

zFound=False
currentNode="AAA"
insPtr=0
steps=0

while not zFound:
    print("Looking at:"+currentNode,end="")
    left,right=map[currentNode]
    print("  Left:"+left,end="")
    print("  Right:"+right)

    instruction=instructions[insPtr]
    print("Instruction:"+instruction)
    steps+=1

    insPtr+=1
    if insPtr>=len(instructions):
        insPtr=0

    if instruction=="L":
        currentNode=left
    elif instruction=="R":
        currentNode=right

    if currentNode=="ZZZ":
        zFound=True
        print("ZZZ found after:"+str(steps))