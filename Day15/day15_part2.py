from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day15/data/input.txt', 'r')
lines = file1.readlines()

map=[]

class Box:
    def __init__(self,n):
        self.lenses=[]
        self.focal=[]
        self.number=n

    def printBox(self):
        print("Box: "+str(self.number),end=" ")
        for c,l in enumerate(self.lenses):
            print("["+l+" "+str(self.focal[c])+"]",end="")
        print("->"+str(self.focalPower()))

    # Find the lens if it already exists
    def findLens(self,label):
        for c,l in enumerate(self.lenses):
            if l==label:
                return c
        return None

    # if the lens exists over-ride it, if it doesn't
    # then add it to the end
    def addLens(self,l,f):
        existingIndex=self.findLens(l)

        if existingIndex is None:
            self.lenses.append(l)
            self.focal.append(f)
        else:
            self.focal[existingIndex]=f
        
    def ifExistsRemove(self,l):
        i=self.findLens(l)
        if i is not None:
            self.lenses.pop(i)
            self.focal.pop(i)

    def focalPower(self):
        b=self.number+1
        total=0
        t=0
        for i,f in enumerate(self.focal):
            t=b*(i+1)*f
            total+=t

        return total




boxes=[]

for i in range(0,256):
    boxes.append(Box(i))

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    parts=lines[c].split(",")

    for p in parts:
        map.append(p)

print("**** DATA LOAD COMPLETE, starting run")

for m in map:
    print(m)

    assignFound=False
    subtractionFound=False

    if "=" in m:
        print("= found")
        parts=m.split("=")
        assignFound=True
    elif "-" in m:
        print("- found")
        parts=m.split("-")
        subtractionFound=True

    cValue=0
    cValueUnset=True
    for c in parts[0]:
        #print("-->"+c+" ASCII:"+str(ord(c)))
        if cValueUnset:
            cValue=ord(c)
            cValueUnset=False
        else:
            cValue=cValue+ord(c)
        cValue*=17
        cValue=cValue%256

    print("cValue->"+str(cValue))

    boxes[cValue].printBox()

    # Everything is decoded now, so lets update the
    # boxes
    if assignFound:
        boxes[cValue].addLens(parts[0],int(parts[1]))

    if subtractionFound:
        boxes[cValue].ifExistsRemove(parts[0])

print("**** RUN COMPLETE, box state is:")
total=0
for b in boxes:
    if len(b.lenses)==0:
        continue
    b.printBox()
    total+=b.focalPower()

print("Total power is: "+str(total))
