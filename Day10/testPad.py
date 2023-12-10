# load a text file
# read file input.txt into an array of strings
file1 = open('Day10/data/test_output.txt', 'r')
lines = file1.readlines()

sum=0
# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()
    lines[c]=lines[c].replace("  ","")
    print(lines[c])
    sum+=len(l)

print(sum)

half=sum/2

print(half)

#8834 - too high
#estimated loop size: 17670
#half way 8835.0