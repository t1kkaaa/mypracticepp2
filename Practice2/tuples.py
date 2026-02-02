#1
thistuple = ("apple",)
print(type(thistuple))

#NOT a tuple
thistuple = ("apple")
print(type(thistuple))

#2
mytuple = ("apple", "banana", "cherry")
print(type(mytuple))

#3
x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)
print(x)

#4
thistuple = ("apple", "banana", "cherry")
del thistuple
print(thistuple)

#5
fruits = ("apple", "mango", "papaya", "pineapple", "cherry")

(green, *tropic, red) = fruits

print(green)
print(tropic)
print(red)

#6
thistuple = ("apple", "banana", "cherry")
for x in thistuple:
  print(x)

#7
thistuple = ("apple", "banana", "cherry")
for i in range(len(thistuple)):
  print(thistuple[i])

#8
thistuple = ("apple", "banana", "cherry")
i = 0
while i < len(thistuple):
  print(thistuple[i])
  i = i + 1

