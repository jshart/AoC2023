class ScratchCard:
    def __init__(self,line):
        self.count=1
        self.winningNumbers=[]
        self.yourNumbers=[]
        self.cardNumber=0

        parts=line.split(":")
        cardNumber=int(parts[0])
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
        if matches==0:
            return 0
        else:
            matches-=1
        return(1<<matches)

# load a text file
# read file input.txt into an array of strings
file1 = open('Day4/data/input.txt', 'r')
lines = file1.readlines()

cards=[]

for c in enumerate(lines):
    lines[c[0]]=lines[c[0]].strip()
    print(lines[c[0]])
    cards.append(ScratchCard(lines[c[0]]))

total=0
for c in cards:
    c.printCard()
    total+=c.checkWinningNumbers()
    print("Matches:"+str(c.checkWinningNumbers()))


print("Total:"+str(total))

