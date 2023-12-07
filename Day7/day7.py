from enum import Enum

# This enum allows us to track the Hand Category
class HandCategory(Enum):
    Undefined = 0
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1

class CardHand:
    def __init__(self,line):
        parts=line.split(' ')
        self.card=parts[0]
        self.rank=parts[1]
        self.count=self.countLetters()
        self.handCat=self.category()

    def print(self):
        print(self.card,self.rank)
        print(self.count)
        print(self.handCat)


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

# Lets just clean up the input data and dump it to terminal
# so we know it loaded ok.
for c in enumerate(lines):
    lines[c[0]]=lines[c[0]].strip()
    cards.append(CardHand(lines[c[0]]))

sum=0
for c in cards:
    c.print()



