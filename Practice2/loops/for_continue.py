#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        continue
    print(x)

#2
for x in range(6):
    if x == 3:
        continue
    print(x)

#3
for char in "code":
    if char == "o":
        continue
    print(char)

#4
for n in [0, 1, 2, 3]:
    if n == 0:
        continue
    print(n)

#5
for i in range(10):
    if i % 2 != 0:
        continue
    print(i)
