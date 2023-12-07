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

    def sort(self):
        self.hands.sort()

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
        self.bid=parts[1]
        self.jokers=0
        self.count=self.countLetters()
        self.handCat=self.category()

    def __lt__(self,other):
        return self.card<other.card

    def print(self):
        print("p----------------------q")
        print(self.card+" "+self.bid+" J:"+str(self.jokers))
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

        if '1' in count:
            self.jokers=count['1']
        return count
    
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
        fiveFound=False
        fourFound=False
        threeFound=False
        twoFound=False
        pairs=0
        j=0
        for i in self.count:
            if i=='1':
                # we found some jokers, so keep them to one side
                j=self.count[i]
            elif self.count[i]==5:
                fiveFound=True
            elif self.count[i]==4:
                fourFound=True
            elif self.count[i]==3:
                threeFound=True
            elif self.count[i]==2:
                twoFound=True
                pairs+=1

        # Now that we know how many jokes we have in play, we need
        # to think about how we "upgrade" this hand to the best we
        # can.
        if j>0:
            # ok we have some jokers
            if j==5:
                # if we have 5 jokers we need to upgrade to five of a kind
                # as we know we can make any hand we like
                cat=HandCategory.FiveOfAKind
            elif j==4:
                # if we have 4 jokers we need to upgrade to five of a kind
                # as the 4 jokers can just match the one other remaining card
                cat=HandCategory.FiveOfAKind
            elif j==3:
                # if we have 3 or 2 of a kind we can upgrade to five of a kind
                if threeFound or twoFound:
                    cat=HandCategory.FiveOfAKind
            elif j==2:
                # if we have three of a kind we can upgrade to a full house, by
                # using the jokers as a pair
                if threeFound:
                    cat=HandCategory.FullHouse
                elif twoFound:
                    # if we have two of a kind we can upgrade to a four of a kind
                    cat=HandCategory.FourOfAKind
                else:
                    # all other cards must be different, so we can upgrade to a three
                    # of a kind by using the 2 jokers
                    cat=HandCategory.ThreeOfAKind
            elif j==1:
                # we only have one joker, so lets see how we can upgrade the hands
                if fourFound:
                    # if we have a four of a kind, we can upgrade to a five of a kind
                    cat=HandCategory.FiveOfAKind
                elif threeFound:
                    # if we have a three of a kind, we can upgrade to a full house
                    cat=HandCategory.FourOfAKind
                elif twoFound:
                    # we found at least one pair, but if we have 2 pairs we can upgrade
                    # to a full house
                    if pairs==2:
                        cat=HandCategory.FullHouse
                    else:
                        # we only have one pair, and one joker, so we can only upgrade
                        # to a three of a kind
                        cat=HandCategory.ThreeOfAKind
                else:
                    # no pairs were found, so we can only upgrade to a two pair
                    cat=HandCategory.TwoPair

        return(cat)

# load a text file
# read file input.txt into an array of strings
file1 = open('Day7/data/input.txt', 'r')
lines = file1.readlines()

cards=[]

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    # Replace K with Z, so we can do an alphabetical < or > and it actually make sense
    lines[c]=lines[c].replace("K","X")
    lines[c]=lines[c].replace("A","Z")
    lines[c]=lines[c].replace("T","B")
    lines[c]=lines[c].replace("J","1")

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
    h.sort()
    h.print()


print("******* two phase sorting done, now printing in order")

sum=0
rank=0
for h in handSorter:
    for c in h.hands:
        rank+=1
        print(c.card)
        sum+=(rank*int(c.bid))

print("Sum:"+str(sum))


#248568809 too low