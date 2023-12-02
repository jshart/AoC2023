# load a text file
# read file input.txt into an array of strings
file1 = open('Day1/data/input2_test.txt', 'r')
lines = file1.readlines()

print("*** STARTING RUN ***")
# create a list with the words "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
words=["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

print(words)

def checkWord(line,words):
    # loop through each character in the line starting from the beginning
    for i, c in enumerate(line):
        # check each word in words to see if it matches the substring starting at this character
        for j, word in enumerate(words):
            if line[i:].startswith(word):
                print("CW:"+word, i, j)
                return(word, i, j+1)
            
    return("none", i, 10)

# do the same search but now start from the end of the string and work backwards
def checkWordBackwards(line,words):
    for i in range(len(line)-1, -1, -1):
        # check each word in words to see if it matches the substring starting at this character)
        for j, word in enumerate(words):
            if line[i:].startswith(word):
                print("CWB:"+word, i, j)
                return(word, i, j+1)
            

total=0
# for each line in the array print the line
for line in lines:
    line = line.strip()  # remove leading and trailing whitespace
    print("["+line+"] [Len="+str(len(line))+"]")

    # for each character in line starting from the beginning search for a digit
    # if a digit is found, print the character and the index of the character
    for i, c in enumerate(line):
        firstDigit=i

        if c.isdigit():
            print(c, i)
            s=c
            break
        firstDigit=firstDigit+1
 
    word, firstWord, wordAsInt = checkWord(line,words)

    if firstDigit < firstWord:
        print("CStart="+s)
    else:
        print("WStart="+str(wordAsInt))

    # repeat the same search but working backwards from the end of the line
    for i, c in enumerate(line[::-1]):
        lastDigit=i

        if c.isdigit():
            print(c, i)
            e=c
            break

    word, lastWord, wordAsInt = checkWordBackwards(line,words)

    if lastDigit > lastWord and lastDigit < len(line):
        print("CEnd="+s+" LastDigit="+str(lastDigit))
    else:
        print("WEnd="+str(wordAsInt))

    ans = s+ e
    print(ans)
    total += int(ans)

print(total)