f = open('17_7717.txt')
a = [int(i) for i in f]
b = []
chet = 0
nechet = 0
maximum = 0
k = 0
for i in a:
    for j in str(i):
        if int(j) % 2 == 0:
            chet += 1
        else:
            nechet += 1
    if chet == nechet:
        if i > maximum:
            maximum = i
for x in range(len(a) - 1):
    chislo_odin = x
    chislo_dva = x + 1
    for i in str(a[chislo_odin]):
        for j in str(a[chislo_dva]):
            if int(i) > int(j):
                k += 1
            else:
                k = 0
                break
        if k == len(str(a[chislo_odin])):
            k = 0
            b.append(str(a[chislo_odin]))
print(b)
