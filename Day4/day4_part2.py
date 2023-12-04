class ScratchCard:
    def __init__(self,line):
        self.count=1
        self.winningNumbers=[]
        self.yourNumbers=[]
        self.cardNumber=0

        parts=line.split(":")
        self.cardNumber=int(parts[0])
        parts2=parts[1].split("|")

        self.addWinningNumbers(parts2[0])
        self.addYourNumbers(parts2[1])

    def addWinningNumbers(self, winNumbers):
        nums=winNumbers.split(' ')
        for n in nums:
            self.winningNumbers.append(int(n))

    def addYourNumbers(self, yourNumbers):
        nums=yourNumbers.split(' ')
        for n in nums:
            self.yourNumbers.append(int(n))

    def printCard(self):
        print(self.cardNumber)
        print(self.count)
        print(self.winningNumbers)
        print(self.yourNumbers)
        print("-----")

    def checkWinningNumbers(self):
        matches=0
        for n in self.winningNumbers:
            if n in self.yourNumbers:
                matches+=1
        return(matches)

# load a text file
# read file input.txt into an array of strings
file1 = open('Day4/data/input.txt', 'r')
lines = file1.readlines()

cards=[]

# Build the deck from the input data
for c in enumerate(lines):
    lines[c[0]]=lines[c[0]].strip()
    print(lines[c[0]])
    cards.append(ScratchCard(lines[c[0]]))

# Walk the deck, expanding the cards
for c in cards:
    c.printCard()
    m=c.checkWinningNumbers()
    for a in range(c.cardNumber,c.cardNumber+m):
        cards[a].count+=c.count

# Could do this above, but just to make it easier to read
# now lets do a second pass counting up the total final cards
total=0
for c in cards:
    print("card:"+str(c.cardNumber)+" has "+str(c.count)+" cards")
    total+=c.count

print("Total:"+str(total))