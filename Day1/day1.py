# load a text file
# read file input.txt into an array of strings
file1 = open('Day1/data/input.txt', 'r')
lines = file1.readlines()

total=0
# for each line in the array print the line
for line in lines:
    line = line.strip()  # remove leading and trailing whitespace
    print(line)

    # for each character in line starting from the beginning search for a digit
    # if a digit is found, print the character and the index of the character
    for i, c in enumerate(line):
        if c.isdigit():
            #print(c, i)
            s=c
            break

    # repeat the same search but working backwards from the end of the line
    for i, c in enumerate(line[::-1]):
        if c.isdigit():
            #print(c, i)
            e=c
            break

    ans = s+ e
    print(ans)
    total += int(ans)

print(total)