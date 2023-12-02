# load a text file
# read file input.txt into an array of strings
file1 = open('Day2/data/input.txt', 'r')
lines = file1.readlines()

#only 12 red cubes, 13 green cubes, and 14 blue cubes
# maxRed=12
# maxGreen=13
# maxBlue=14

total=0

# for each line in the array print the line
for line in lines:
    line = line.strip()  # remove leading and trailing whitespace
    #print(line)
    game, content = line.split(":")
    print("G["+game+"]")
    rounds = content.split(";")

    # for this game reset the max counters
    maxRed=0
    maxGreen=0
    maxBlue=0

    # for each round in this game, check the pulls
    for  round in rounds:
        print("R---["+round+"]")

        pulls = round.split(", ")

        # for each pull in this round, check the colour and number
        for pull in pulls:
            print("P----["+pull+"]")

            number, colour = pull.split(" ")
            number = int(number)
            if colour == "red":
                if number > maxRed:
                    maxRed=number
            elif colour == "green":
                if number > maxGreen:
                    maxGreen=number
            elif colour == "blue":
                if number > maxBlue:
                    maxBlue=number
            else:
                print("error")

    print()

    total+=maxRed*maxGreen*maxBlue
    print("Total: "+str(total))