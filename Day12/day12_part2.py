from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day12/data/input_test.txt', 'r')
lines = file1.readlines()

map=[]

# Lets  clean up the input data
for unknownSpringConditionCount,l in enumerate(lines):
    lines[unknownSpringConditionCount]=lines[unknownSpringConditionCount].strip()
    parts=lines[unknownSpringConditionCount].split(' ')
    guide=parts[1].split(',')

    map.append([parts[0]*5,guide*5])
    #map.append([parts[0],guide])


for m in map:
    print(m)
print("**** LOAD COMPLETE and ready to start processing")

totalGoodCandidateCount=0

totalMasksToTest=0
for m in map:
    print(m,end="")

    guideTotal=0
    # for debug/cross-check, lets cound the number of bad springs
    # in the guide, so we can do a sanity check at the end
    for g in m[1]:
        guideTotal+=int(g)

    # How many unknows do we have in the string?
    unknownSpringConditionCount=m[0].count('?')
    knownGoodSpringConditionCount=m[0].count('.')
    knownBadSpringConditionCount=m[0].count('#')


    # Create a max binary mask size from this
    maxMaskSize=(1<<unknownSpringConditionCount)
    minMaskSize=maxMaskSize>>1

    print(" unknown="+str(unknownSpringConditionCount)+" Max Mask Size="+str(maxMaskSize),end=" Masks:")

    masks=[]
    candidates=[]
    goodCandidates=[]

    # TODO - can we optimise this by starting i at a higher position and skipping most of the known
    # smaller/bad masks

    # for each possible mask permuation lets generate a mask
    #for i in range(minMaskSize,maxMaskSize+1):
    for i in range(0,maxMaskSize+1):

        # Convert this index to an actual binary number and strip the 0b prefix
        b=bin(i)[2:]

        if len(b)<unknownSpringConditionCount:
            b=b.zfill(unknownSpringConditionCount)

        #print("["+b+"]",end="")
        totalMasksToTest+=1
        masks.append(b)

#print("["+masks[0]+"]...["+masks[-1]+"]")
        candidate=""
        maskSubIndex=0
        for c in m[0]:
            if c=='?' and b[maskSubIndex]=='0':
                candidate+="#"
                maskSubIndex+=1
            elif c=='?' and b[maskSubIndex]=='1':
                candidate+='.'
                maskSubIndex+=1
            else:
                candidate+=c


        parts = candidate.split('.')
        damagedSpringCount=0
        badMatch=False
        for p in parts:
            if len(p)<1:
                continue
            if p[0]=='#':
                # have we exceeded the expect count of damaged spring
                # areas? if so then we know ths is bad.
                if damagedSpringCount>=len(m[1]):
                    badMatch=True
                    break

                # Damaged spring found, does its size match our guide?
                if len(p)!=int(m[1][damagedSpringCount]):
                    # this is a bad match
                    badMatch=True
                    break

                else:
                    # looks good, lets move on to the next spring
                    damagedSpringCount+=1

        # did we consume all of the guide numbers?
        if damagedSpringCount<len(m[1]):
            badMatch=True

        if not badMatch:
            # Looks good, lets print this as a good candidate
            print("Good candidate: "+candidate+" damaged areas found:"+str(damagedSpringCount),end="")
            if candidate.count('#')==guideTotal:
                print(" (PASSED cross check)")
            else:
                print(" (FAILED cross check)")
                exit

            if candidate not in goodCandidates:
                goodCandidates.append(candidate)
                totalGoodCandidateCount+=1
            else:
                print("Dropping as dup")

print("Total masks to test="+str(totalMasksToTest))
print("Total good candidate count="+str(totalGoodCandidateCount))
