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

currentNodes=[]

for k in map:
    if (k[2]=='A'):
        currentNodes.append(k)

print("Starting Node List:",end="")
print(currentNodes)

zFound=False
insPtr=0
steps=0

minZ=[0,0,0,0,0,0]

while not zFound:

    # Instruction processing is the same for all threads
    instruction=instructions[insPtr]
    #print("Instruction:"+instruction)
    steps+=1
    insPtr+=1
    if insPtr>=len(instructions):
        insPtr=0

    # Assume we've ended until the code tells us otherwise
    zFound=True
    for i,currentNode in enumerate(currentNodes):
       
        #print("Looking at:"+currentNode,end="")
        left,right=map[currentNode]
        #print("  Left:"+left,end="")
        #print("  Right:"+right)

        if instruction=="L":
            currentNodes[i]=left
        elif instruction=="R":
            currentNodes[i]=right

        if currentNodes[i][2] !="Z":
            pass
        else:
            minZ[i]=steps

    for z in minZ:
        if z==0:
            zFound=False
            break

    if steps % 1000000 == 0:
        print("Steps:"+str(steps))

print("All Z's found after:"+str(steps))

print(minZ)
r=0
il=len(instructions)
for z in minZ:
    r=z % il
    print(r)

#118200000000
#23355229540361858900885867