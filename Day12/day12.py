from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day12/data/input.txt', 'r')
lines = file1.readlines()

map=[]

# Lets  clean up the input data
for unknownSpringConditionCount,l in enumerate(lines):
    lines[unknownSpringConditionCount]=lines[unknownSpringConditionCount].strip()
    parts=lines[unknownSpringConditionCount].split(' ')
    guide=parts[1].split(',')

    map.append([parts[0],guide])

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

    print(" unknown="+str(unknownSpringConditionCount)+" Max Mask Size="+str(maxMaskSize),end=" Masks:")

    masks=[]
    # for each possible mask permuation lets generate a mask
    for i in range(maxMaskSize+1):

        # Convert this index to an actual binary number and strip the 0b prefix
        b=bin(i)[2:]

        # Only print the masks if they are exactly the lenth of the unknowns
        # TODO - There is a bug here that this will prune too many masks - specifically
        # it'll prune ones where the leading digits are zero - which is too aggressive.
        # need to rework this to front bad with 0's
        if len(b)<unknownSpringConditionCount:
            b=b.zfill(unknownSpringConditionCount)

        #print("["+b+"]",end="")
        totalMasksToTest+=1
        masks.append(b)
    print("["+masks[0]+"]...["+masks[-1]+"]")

    # Next we need to complete the unknowns in the input string using the masks we just generated
    # in order to create a series of candidate strings which we can then test the numeric guide
    # against to see if they are valid
    candidates=[]
    for mask in masks:
        candidate=""
        maskSubIndex=0
        for c in m[0]:
            if c=='?' and mask[maskSubIndex]=='0':
                candidate+="#"
                maskSubIndex+=1
            elif c=='?' and mask[maskSubIndex]=='1':
                candidate+='.'
                maskSubIndex+=1
            else:
                candidate+=c
        #if candidate not in candidates:
        candidates.append(candidate)

    print("Final set of candidate strings for:"+m[0]+" is:")
    #print(candidates)

    goodCandidates=[]
    # lets check the candidates to see which ones meet our criteria
    for candidate in candidates:
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




# TODO Theory - what if we generate every possible combination of #/. to replace the ?
# then loop through, applying the numeric rules to see which ones are valid and which
# ones are invalid?
# One optimisation is that we know we have an exact count of the number of operational
# springs, so we can immediately eliminate any that have more or less than that.

# Theory is probably good, but I've got some edge case causing a problem. Current output
# is too high (7110) as is (7100)
# 7000 is too low
# so its been 7000 and 7100
# 7050,7091 is wrong