time=35937366
distance=212206012011044

#time=71530
#distance=940200
winCounts=[]

print("---- Searching for left hand border")
# lets test every button hold time
for buttonHoldTime in range(0,time+1):
    timeLeft=time-buttonHoldTime
    distanceTravelled=timeLeft*buttonHoldTime
    #print(buttonHoldTime,timeLeft,distanceTravelled)
    if distanceTravelled>=distance:
        leftBorder=buttonHoldTime-1
        break

print("---- Searching for right hand border")
for buttonHoldTime in range(time,0,-1):
    timeLeft=time-buttonHoldTime
    distanceTravelled=timeLeft*buttonHoldTime
    #print(buttonHoldTime,timeLeft,distanceTravelled)
    if distanceTravelled>=distance:
        rightBorder=buttonHoldTime
        break

# https://www.wolframalpha.com/input?i=solve+d%3D%28t-b%29*b+for+b
print(leftBorder,rightBorder)
newTotal=rightBorder-leftBorder
print(newTotal)