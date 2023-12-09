from enum import Enum

# load a text file
# read file input.txt into an array of strings
file1 = open('Day9/data/input.txt', 'r')
lines = file1.readlines()

# Lets  clean up the input data
for c,l in enumerate(lines):
    lines[c]=lines[c].strip()

# parse the numbers into arrays of ints
baseNumbers=[]
temp=[]
answers=[]
for l in lines:
    parts=l.split(" ")
    temp.clear()
    for p in parts:
        temp.append(int(p))
    baseNumbers.append(temp.copy())

print("**** Parsing complete")

# lets parse each row
total=0
for i,b in enumerate(baseNumbers):
    print("**** Processing:"+str(i))

    done=False
    rows=[]
    row=[]
    rows.append(b.copy())
    while not done:
        done=True
        row.clear()
        b=rows[-1]
        for num in range(0,len(b)-1):
            a=b[num+1]-b[num]
            row.append(a)
            if len(row)>2:
                if row[-1]!=row[-2]:
                    done=False
        rows.append(row.copy())

    # just put a zero in the last row, to make the loop
    # and math easier for the final answers.
    rows.append([0])

    print("**** Finished processing row, output:")
    sum=0
    for r in range(len(rows)-1,-1,-1):
        print("Rn:"+str(r),end=" ")
        print(rows[r],end="")
        print(" Target:"+str(rows[r][-1]))

        # make sure we dont over flow the array
        if r>0:
            # TODO work out how to add up the ends of the 2 rows
            rows[r-1].append(rows[r][-1]+rows[r-1][-1])
            print("Adding:"+str(rows[r-1][-1]))

    for r in rows:
        print(r)

    answers.append(rows[0][-1])

print("**** Answers:")

for a in answers:
    print(a)
    total=total+a
    
print("**** Total:"+str(total))

