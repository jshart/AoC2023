# load a text file
# read file input.txt into an array of strings
file1 = open('Day3/data/input.txt', 'r')
lines = file1.readlines()
for c in enumerate(lines):
    lines[c[0]]=lines[c[0]].strip()

# create a function that will check the letters around a given
# substring for non numeric and non peroid characters
def checkLetters(lines, lineNum, charNumStart, charNumEnd):
    # startLine equals line if its greater than 0, otherwise it equals 0
    startLine=lineNum-1 if lineNum>0 else 0
    # endLine equals line if its less than the length of the array, otherwise it equals the length of the array
    endLine=lineNum+1 if lineNum<len(lines)-1 else len(lines)-1
    # startChar equals charNumStart if its greater than 0, otherwise it equals 0
    startChar=charNumStart-1 if charNumStart>0 else 0
    # endChar equals charNumEnd if its less than the length of the line, otherwise it equals the length of the line
    endChar=charNumEnd+1 if charNumEnd<len(lines[0]) else len(lines[0])

    print("--Range:"+str(startLine)+","+str(endLine)+","+str(startChar)+","+str(endChar))

    for i in range(startLine, endLine+1):
        line=lines[i]
        print("--|"+line[startChar:endChar])

        for j in range(startChar, endChar):
            #print("-->"+line[j], end="")
            if line[j].isdigit():
                # This *should* be the number we're checking
                # Possble edge case I may need to think about
                # is if there any numbers adjacent but it doesnt
                # look like this is so.
                pass
            elif line[j]==".":
                # This is a period, so we can skip it
                pass
            else:
                # This is any other character, which makes this number valid - return True
                print("--V["+line[j]+"]")
                return True
            
    # if we get to the end of the function with no return, then the number is invalid
    return False

inNumber=False
validSum=0
invalidSum=0

invalidNumbers=[]

for lineNum, line in enumerate(lines):
    print(line)
    for charNum, c in enumerate(line):
        if c.isdigit():
            if inNumber:
                # already in a number, continue to track it
                pass
            else:
                # start tracking a number
                inNumber=True
                charNumStart=charNum
        else:
            if inNumber:
                # we're in a number currently, and have now
                # found a non-digit character, so we're done
                inNumber=False
                print("Found:"+line[charNumStart:charNum])
                if checkLetters(lines, lineNum, charNumStart, charNum):
                    print(" is valid")
                    # this number is valid, so add it to the sum
                    validSum=validSum+int(line[charNumStart:charNum])
                else:
                    print(" is invalid")
                    invalidSum=invalidSum+int(line[charNumStart:charNum])
                    invalidNumbers.append(line[charNumStart:charNum])
            else:
                # not in a number, and still not in a number
                # so do nothing
                pass

    # if we exit the loop still in a number then it means there
    # is a number at the end of the line, so we need to check it
    if inNumber:
        inNumber=False
        charNum+=1
        print("Found:"+line[charNumStart:charNum])
        if checkLetters(lines, lineNum, charNumStart, charNum):
            print(" is valid on edge")
            # this number is valid, so add it to the sum
            validSum=validSum+int(line[charNumStart:charNum])
        else:
            print(" is invalid on edge")
            invalidSum=invalidSum+int(line[charNumStart:charNum])
            invalidNumbers.append(line[charNumStart:charNum])



# max: value (always return valid): Sum:602481
# Sum:552774 (too high)
# Sum:548142 (too low)
# Sum:548567 (too low)
# "losing" a max of 4207 to erronous invalid cases

print("Valid Sum:"+str(validSum))
print("Invalid Sum:"+str(invalidSum))

print("Invalid Numbers:"+str(invalidNumbers))

# Found:406
# --Range:129,131,79,84
# --|.....
# --V[%]
#  is valid