#      a1  a2 a3
from decimal import Decimal
import decimal
p = [0, 0.042, 0.083, 0.125, 0.042, 0.042, 0.042, 0.042, 0.042, 0.125, 0.042, 0.083, 0.042, 0.042, 0.042, 0.042, 0.083, 0.042]
p = [decimal.Decimal(i) for i in p]
print(len(p))
s =  "10 4 2  5"

popka = [[]]

buf = 0

for i in range(len(p)-1):
  c = p[i+1]
  popka.append([buf,buf+c])
  buf += c
print(popka)
print(len(s.split()))
r = [0,1]
c = 0
suka = []
for i in [int(i) for i in s.split()]:
  suka.append(r[::])
  print(c,r)
  d = r[1]-r[0]
  print(i)
  r[1] = round(r[0]+popka[i][1]*d,20)
  r[0] = round(r[0]+popka[i][0]*d,20)
  c+=1
print(c,r)
for i in range(4):
  print(suka[i][0])
print()
for i in range(4):
  print(suka[i][1])
