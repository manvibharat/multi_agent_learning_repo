li1 = [20,40,10,50]

li2 = [100 -i for i in li1]

quant_inx = sorted(range(len(li1)), key=lambda k:li1[k], reverse=True)

li1_sorted = [li1[i] for i in quant_inx]
li2_sorted = [li2[i] for i in quant_inx]


print(li1_sorted)
print(li2_sorted)

i =2

if i in [1,2,3]:
    print("true")

non_deviating = list(range(0,4))

print(non_deviating)


for i in range(6):
    if i == 2:
        i = i+2
    print(i)