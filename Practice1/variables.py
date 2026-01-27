#1
x = str(3)   
y = int(3)   
z = float(3) 
print(x)
print(y)
print(z)

#2
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

#3
x = 5
y = "John"
print(x, y)

#4
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()
print("Python is " + x)

#5
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()
print("Python is " + x)

#6
def myfunc():
  global x
  x = "fantastic"

myfunc()
print("Python is " + x)
