mylist = [1,2,3,4,5]

for num in mylist:
    print(num)

    if num==5:
        mylist.append(6)
        mylist.remove(5)
        
l=[]

b=[1,2]

l.append(b)

b[0]=4

print(l)