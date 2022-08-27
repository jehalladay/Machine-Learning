n = int(input())
seq = [n]

for i in range(n):
    if(i==1 or i == 0): 
        continue
    else:
        while (n%i == 0):
            n = n/i
            seq.append(int(n))
    if(n == 1):
        break

seq.reverse()
print(len(seq))
for i in seq:
    print(i, end=' ')
    