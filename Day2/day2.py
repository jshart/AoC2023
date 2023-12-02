# load a text file
# read file input.txt into an array of strings
file1 = open('Day2/data/input.txt', 'r')
lines = file1.readlines()

#only 12 red cubes, 13 green cubes, and 14 blue cubes
maxRed=12
maxGreen=13
maxBlue=14

total=0

# for each line in the array print the line
for line in lines:
    line = line.strip()  # remove leading and trailing whitespace
    #print(line)
    game, content = line.split(":")
    print("G["+game+"]")
    rounds = content.split(";")
    legalRound=True

    for  round in rounds:
        print("R---["+round+"]")

        pulls = round.split(", ")
        legalHand=True

        for pull in pulls:
            print("P----["+pull+"]")

            number, colour = pull.split(" ")
            number = int(number)
            if colour == "red":
                if number > maxRed:
                    legalHand=False
            elif colour == "green":
                if number > maxGreen:
                    legalHand=False
            elif colour == "blue":
                if number > maxBlue:
                    legalHand=False
            else:
                print("error")
        print("P----["+str(legalHand)+"]")

        if not legalHand:
            legalRound=False

    if legalRound:
        total+=int(game)
    print()

print("Total: "+str(total))