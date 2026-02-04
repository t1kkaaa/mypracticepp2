#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    if x == "banana":
        break
    print(x)

#2
for x in range(10):
    if x == 5:
        break
    print(x)

#3
for char in "Python":
    if char == "h":
        break
    print(char)

#4
nums = [1, 2, 3, 4, 5]
for n in nums:
    print(n)
    if n == 3:
        break

#5
for i in range(1, 100):
    print(i)
    break
