# https://www.redblobgames.com/pathfinding/a-star/introduction.html

from enum import Enum
import math
testing=False

# Theory - the circuit is a binary counter (or series of smaller counters)
# some number of passes through this gets us to a number that will cause
# a low signal to Rx

# create an enum for the compass cardinal directions
class WallState(Enum):
    Outside=0
    Onwall=1
    Inside=2

class PulseTypes(Enum):
    noPulse=-1
    lowPulse=0
    highPulse=1


class Module:
    def __init__(self,raw):
        self.type=raw[0]
        parts=raw[1:].split("->")
        self.moduleName=parts[0]
        self.outputs=parts[1].split(",")
        self.inputs={}
        self.flipFlopState=PulseTypes.lowPulse

    def execute(self,e):
        returnEvents=[]
        if self.type=="#":
            # broadcaster
            for o in self.outputs:
                returnEvents.append(Event(self.moduleName,e.pulse,o))
            pass
        elif self.type=="%":
            #print("--> FlipFlop processing event:",end="")
            #e.print()
            if e.pulse==PulseTypes.lowPulse:
                if self.flipFlopState==PulseTypes.highPulse:
                    self.flipFlopState=PulseTypes.lowPulse
                else:
                    self.flipFlopState=PulseTypes.highPulse

                for o in self.outputs:
                    returnEvents.append(Event(self.moduleName,self.flipFlopState,o))
                    #print("--> FlipFlop",self.moduleName,"->",self.flipFlopState,end="")
                    #print("->",o)
        elif self.type=="&":
            # conjunction
            #print("--> Conjunction processing event:",end="")
            #e.print()
            self.inputs[e.src]=e.pulse

            allHigh=True
            for i in self.inputs:
                if self.inputs[i]==PulseTypes.lowPulse:
                    allHigh=False

            if allHigh:
                outputPulse=PulseTypes.lowPulse
            else:
                outputPulse=PulseTypes.highPulse

            for o in self.outputs:
                returnEvents.append(Event(self.moduleName,outputPulse,o))
                #print("--> Conjunction",self.moduleName,"->",outputPulse)
            pass
        else:
            # Other
            pass

        return returnEvents
            

    def print(self):
        print(self.type,self.moduleName)
        print("In->",end="")
        print(self.inputs)
        print("Out->",end="")
        print(self.outputs)

class Event:
    def __init__(self, src, pulse, dest):
        self.src=src
        self.pulse=pulse
        self.dest=dest

    def print(self):
        print(self.src,"=>",self.pulse,"=>",self.dest)


def summariseFlipFlops(modules):
    sum=""
    for m in modules:
        if modules[m].type=="%":
            if modules[m].flipFlopState==PulseTypes.lowPulse:
                sum+="0"
            else:
                sum+="1"
        else:
            pass
    return sum
        
modules={}
# load a text file
# read file input.txt into an array of strings
if testing:
    file1 = open('Day20/data/input_test2.txt', 'r')
    lines = file1.readlines()
else:
    file1 = open('Day20/data/input.txt', 'r')
    lines = file1.readlines()


for c,l in enumerate(lines):
    l=l.strip()
    l=l.replace(" ","")
    print(l)
    temp=Module(l)
    modules[temp.moduleName]=temp

# Lets cross reference the inputs to the modules
# for each module...
for m in modules:
    modules[m].print()
    
    # check each of the output names...
    for o in modules[m].outputs:
        # if this output exists as a module in the list
        # lets link this module to the one it outputs to
        if o in modules:
            modules[o].inputs[m]=PulseTypes.lowPulse
        else:
            print("Output",o,"does not exist")

#print("*** Final connection list:")
for m in modules:
    modules[m].print()

maxButtonPresses=1000
buttonPresses=1
lowCount=0
highCount=0
done=False

while not done:
    #print()
    #print("*** Start of execution run, press:"+str(buttonPresses))
    eventList=[]
    eventList.append(Event("Button",PulseTypes.lowPulse,"broadcaster"))
    ticks=0
    while len(eventList)>0 and ticks<100:
        # for each event in the event list...
        returnEvents=[]

        for e in eventList:
            #print("Processing event:",end="")
            #e.print()
            if e.pulse==PulseTypes.lowPulse:
                lowCount+=1
            elif e.pulse==PulseTypes.highPulse:
                highCount+=1

            # if the event is for a module in the list
            if e.dest in modules:
                # execute the module
                # get the return events
                #print("--> Executing for:"+e.dest)
                returnEvents+=modules[e.dest].execute(e)

                # if returnEvents==None:
                #     pass
                #     print("No return events")
                # else:
                #     for r in returnEvents:
                #         print("  RE-->",end="")
                #         r.print()
            else:
                #print("Event destination",e.dest,"does not exist, trying to pass",end="")
                #print(e.pulse)
                if e.pulse==PulseTypes.lowPulse:
                    print("*** DONE ***")
                    print("Tick",ticks,"New Events:",len(returnEvents),end="")
                    print(" Low Pulse Count:"+str(lowCount),end="")
                    print(" High Pulse Count:"+str(highCount))
                    print("Button presses (0 start):"+str(buttonPresses))

                    done=True

        #ticks+=1
        # print("Tick",ticks,"New Events:",len(returnEvents),end="")
        # print(" Low Pulse Count:"+str(lowCount),end="")
        # print(" High Pulse Count:"+str(highCount))
        eventList.clear()
        eventList=returnEvents

    print("FF state:"+summariseFlipFlops(modules))

    if buttonPresses % 20 == 0:
        print("Button heart beat:"+str(buttonPresses))
        done=True

    buttonPresses+=1

sum=lowCount*highCount
print("Final sum of pulses is "+str(sum))

