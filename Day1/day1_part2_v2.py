# load a text file
# read file input.txt into an array of strings
file1 = open('Day1/data/input.txt', 'r')
lines = file1.readlines()

print("*** STARTING RUN ***")
# create a list with the words "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
words=["zero","one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

print(words)

# create a function that will return the list index for a given word in words
def findWord(words,word):
    for i, w in enumerate(words):
        if w == word:
            return str(i)
    return str(-1)

def checkWord(line,words):
    # loop through each character in the line starting from the beginning
    for i, c in enumerate(line):
        # check each word in words to see if it matches the substring starting at this character
        for j, word in enumerate(words):
            if line[i:].startswith(word):
                return(word)
            
# do the same search but now start from the end of the string and work backwards
def checkWordBackwards(line,words):
    for i in range(len(line)-1, -1, -1):
        # check each word in words to see if it matches the substring starting at this character)
        for j, word in enumerate(words):
            if line[i:].startswith(word):
                return(word)


total=0
for line in lines:
    line=line.strip()
    print("["+line+"]")

    for i in range(0,10):
        line=line.replace(str(i),words[i])
    print("--- {"+line+"}")

    # find first number word in line
    firstWord = checkWord(line,words)
    print("--- First Word="+firstWord)

    # find first number word in line
    lastWord = checkWordBackwards(line,words)
    print("--- Last Word="+lastWord)

    ans=findWord(words,firstWord)+findWord(words,lastWord)
    print("--- STR="+ans)

    total += int(ans)

print("Final answer: "+str(total))
#29, 83, 13, 24, 42, 14, and 76


            
