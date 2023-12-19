# https://www.redblobgames.com/pathfinding/a-star/introduction.html

from enum import Enum
import math
testing=False

# create an enum for the compass cardinal directions
class WallState(Enum):
    Outside=0
    Onwall=1
    Inside=2


# Example rules:
# px{a<2006,qkq,m>2090,A,rfg}
# pv{a>1716,R,A}
# lnx{m>1548,A,A}
# rfg{s<537,gd,x>2440,R,A}
# qs{s>3448,A,lnx}
# qkq{x<1416,A,crn}
# crn{x>2662,A,R}
# in{s<1351,px,qqz}
# qqz{s>2770,qs,m<1801,hdj,R}
# gd{a>3333,R,R}
# hdj{m>838,A,pv}
class Rule:
    def __init__(self, rName, r):
        self.name=rName
        self.conditions=r.split(",")
        self.printRule()

    def printRule(self):
        print("Name:"+self.name,end=" == ")
        print(self.conditions,end=" ")
        print()

    # TODO - need to write an evaluation routine that is aware of the CSV list
    # of conditions/sub-conditions.
    def evaluate(self, mPart):
        cIndex=0
        done=False
        while not done:
            if '>' in self.conditions[cIndex]:
                parts=self.conditions[cIndex].split(">")
                if mPart.vars[parts[0]]>int(parts[1]):
                    cIndex+=1
                else:
                    cIndex+=2
            elif '<' in self.conditions[cIndex]:
                parts=self.conditions[cIndex].split("<")
                if mPart.vars[parts[0]]<int(parts[1]):
                    cIndex+=1
                else:
                    cIndex+=2

            # have we now moved onto a sub condition?
            if '>' in self.conditions[cIndex] or '<' in self.conditions[cIndex]:
                # in sub condition, let it loop and re-evaluate the sub-condition
                pass
            else:
                done=True
    
        return self.conditions[cIndex]
    



class MPart:
    def __init__(self, m):
        self.vars={}

        parts=m.split(",")
        for p in parts:
            if p[0]=="s":
                self.vars['s']=int(p[2:])
            elif p[0]=="a":
                self.vars['a']=int(p[2:])
            elif p[0]=="m":
                self.vars['m']=int(p[2:])
            elif p[0]=="x":
                self.vars['x']=int(p[2:])

        self.printPart()

    def printPart(self):
        print("s="+str(self.vars['s']),end=",")
        print("a="+str(self.vars['a']),end=",")
        print("m="+str(self.vars['m']),end=",")
        print("x="+str(self.vars['x']))

    def sumResults(self):
        total=0
        for v in self.vars:
            total+=self.vars[v]

        return total
        

# load a text file
# read file input.txt into an array of strings
if testing:
    file1 = open('Day19/data/input_test.txt', 'r')
    lines = file1.readlines()
else:
    file1 = open('Day19/data/input.txt', 'r')
    lines = file1.readlines()

ruleLines=[]
rules={}
mPartsLines=[]
mParts=[]

processingRules=True
for c,l in enumerate(lines):
    l=l.strip()

    print(l)

    if len(l)==0:
        processingRules=False
        continue

    if processingRules:
        ruleLines.append(l)
    else:
        mPartsLines.append(l)

print("Rules:")
print(ruleLines)
for r in ruleLines:
    parts=r.split("{")
    rules[parts[0]]=Rule(parts[0],parts[1][:-1])

print("MParts:")
print(mPartsLines)
for m in mPartsLines:
    mParts.append(MPart(m[1:-1]))

# Run rules starting with the first in the dict

total=0
for mp in mParts:
    currentRuleName="in"
    done=False
    while not done:
        rules[currentRuleName].printRule()
        retVal=rules[currentRuleName].evaluate(mp)
        if len(retVal)==1:
            done=True
            print("Result: "+retVal)
        else:
            currentRuleName=retVal

    if retVal=="A":
        total+=mp.sumResults()

# print final total
print("Total: "+str(total))
