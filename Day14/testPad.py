def delEven(el):
    for i in el:
        if i%2==0:
            el.remove(i)
    return el

l=[1,2,3,4,5,6,7,8,9]

print(l)
delEven(l)
print(l)


