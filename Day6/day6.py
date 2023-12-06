time=[35,93,73,66]
distance=[212,2060,1201,1044]

#time=[7,15,30]
#distance=[9,40,200]
winCounts=[]

for i,t in enumerate(time):
    print("--------------NEW RACE--------------")
    print("Testing race with max time: "+str(t))
    wins=0

    # lets test every button hold time
    for buttonHoldTime in range(0,t+1):
        timeLeft=t-buttonHoldTime
        distanceTravelled=timeLeft*buttonHoldTime

        print("For Button time:"+str(buttonHoldTime),end="")
        print(" distance travelled:"+str(distanceTravelled))

        if (distanceTravelled > distance[i]):
            wins+=1

    print("Race won: "+str(wins)+" times")
    winCounts.append(wins)

print("All done:")
print(winCounts)
