from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day15/data/input.txt', 'r')
lines = file1.readlines()

map=[]


# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    parts=lines[c].split(",")

    for p in parts:
        map.append(p)

print("**** DATA LOAD COMPLETE, starting run")

hashCodes=[]

for m in map:
    print(m)

    cValue=0
    cValueUnset=True
    for c in m:
        print("-->"+c+" ASCII:"+str(ord(c)))
        if cValueUnset:
            cValue=ord(c)
            cValueUnset=False
        else:
            cValue=cValue+ord(c)
        cValue*=17
        cValue=cValue%256
        
    print("---->"+str(cValue))
    hashCodes.append(cValue)

# Work out the total
total=0
for h in hashCodes:
    total+=h

print("Total: "+str(total))
