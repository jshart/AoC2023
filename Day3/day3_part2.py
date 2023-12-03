# load a text file
# read file input.txt into an array of strings
file1 = open('Day3/data/input.txt', 'r')
lines = file1.readlines()
for c in enumerate(lines):
    lines[c[0]]=lines[c[0]].strip()

gears={}

# create a function that will check the letters around a given
# substring for non numeric and non peroid characters
def checkLetters(gears, lines, lineNum, charNumStart, charNumEnd):
    # startLine equals line if its greater than 0, otherwise it equals 0
    startLine=lineNum-1 if lineNum>0 else 0
    # endLine equals line if its less than the length of the array, otherwise it equals the length of the array
    endLine=lineNum+1 if lineNum<len(lines)-1 else len(lines)-1
    # startChar equals charNumStart if its greater than 0, otherwise it equals 0
    startChar=charNumStart-1 if charNumStart>0 else 0
    # endChar equals charNumEnd if its less than the length of the line, otherwise it equals the length of the line
    endChar=charNumEnd+1 if charNumEnd<len(lines[0]) else len(lines[0])

    numString=lines[lineNum][charNumStart:charNumEnd]

    print("--Range:"+str(startLine)+","+str(endLine)+","+str(startChar)+","+str(endChar))

    for i in range(startLine, endLine+1):
        line=lines[i]
        print("--|"+line[startChar:endChar])

        for j in range(startChar, endChar):
            #print("-->"+line[j], end="")
            if line[j]=="*":
                # found a "gear", return the current co-ordinates of that character
                gearList=gears.get((i,j))
                if gearList is None:
                    gears[(i,j)]=[numString]
                else:
                    gears[(i,j)].append(numString)
                return i,j
            
    return -1,-1

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
                x,y = checkLetters(gears, lines, lineNum, charNumStart, charNum)

                if x>-1 and y>-1:
                    # found a gear
                    print("--Gear:"+str(x)+","+str(y)+" = "+str(line[charNumStart:charNum]))

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
        x,y = checkLetters(gears, lines, lineNum, charNumStart, charNum)

        if x>-1 and y>-1:
            # found a gear
            print("--Gear:"+str(x)+","+str(y)+" = "+str(line[charNumStart:charNum]))


print(gears)

print("Valid cog lists:")
sum=0
total=0
for gear in gears:
    cogList=gears[gear]
    if len(cogList)==2:
        sum=int(cogList[0])*int(cogList[1])
        total+=sum

print("Total:"+str(total))