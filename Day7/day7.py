from enum import Enum

class HandSorter:
    def __init__(self,hCat):
        self.hands=[]
        self.handCat=hCat

    def print(self):
        print("Hands of type:"+self.handCat.name)
        if len(self.hands)==0:
            print("   [No hands]")
        for h in self.hands:
            h.print()

# This enum allows us to track the Hand Category
class HandCategory(Enum):
    Undefined = 0
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7

class CardHand:
    def __init__(self,line):
        parts=line.split(' ')
        self.card=parts[0]
        self.rank=parts[1]
        self.count=self.countLetters()
        self.handCat=self.category()

    def print(self):
        print("p----------------------q")
        print(self.card,self.rank)
        print(self.count)
        print(self.handCat)
        print("b----------------------d")

    # This function creates a count of each
    # different type of letter in the card.
    def countLetters(self):
        count={}
        for c in self.card:
            if c in count:
                count[c]+=1
            else:
                count[c]=1
        return count
    
    def cardValue(self,card):
        if card=='K':
            return(13)
        if card=='Q':
            return(12)
        if card=='J':
            return(11)
        else:
            return(int(card))
    
    # This function puts the hand into a category
    # based on the letters in the card and if they fall
    # into
    def category(self):
        cat=HandCategory.Undefined

        # TODO - Need to implement "full house"

        # Five of a kind, where all five cards have the same label: AAAAA
        # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
        # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
        # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
        # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
        # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
        # High card, where all cards' labels are distinct: 23456
        for i in self.count:
            if self.count[i]==5:
                cat=HandCategory.FiveOfAKind
                break
            elif self.count[i]==4:
                cat=HandCategory.FourOfAKind
                break
            elif self.count[i]==3:
                cat=HandCategory.ThreeOfAKind
                break
        
        if cat==HandCategory.Undefined:
            # lets check how many 2-pairs we have
            pairs=0
            for i in self.count:
                if self.count[i]==2:
                    pairs+=1
            if pairs==2:
                cat=HandCategory.TwoPair
            elif pairs==1:
                cat=HandCategory.OnePair
            else:
                cat=HandCategory.HighCard
        return(cat)

# load a text file
# read file input.txt into an array of strings
file1 = open('Day7/data/input_test.txt', 'r')
lines = file1.readlines()

cards=[]

# Lets  clean up the input data
for c in enumerate(lines):
    lines[c[0]]=lines[c[0]].strip()

# then we load the data into the card class ready to score games
for l in lines:
    cards.append(CardHand(l))
    print(cards[-1].print())

print("******* Card loading, complete, now sorting and organising")

# Lets create a helper class to sort the hands of the same
# type into subcategories, to make the scoring easier.
handSorter=[]
for type in HandCategory:
    handSorter.append(HandSorter(type))
for h in handSorter:
    h.print()

print("******* Hand Categories constructed, now sorting hands")

# For each hand lets add them to the right sorter object
# so they are all grouped by hand type
for c in cards:
    print("--> Processing card:"+c.card)
    handSorter[c.handCat.value].hands.append(c)

print("******* Hand Categories sorted, grouped as")

for h in handSorter:
    h.print()
    print()