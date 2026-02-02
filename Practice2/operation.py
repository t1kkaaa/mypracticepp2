#1
sum1 = 100 + 50     
sum2 = sum1 + 250    
sum3 = sum2 + sum2   
print(sum1)
print(sum2)
print(sum3)

#2
x = 15
y = 4

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y)
print(x ** y)
print(x // y)

#3
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

#4
x = 5
y = 3

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

#5
x = 5

print(x > 0 and x < 10)
print(x < 5 or x > 10)
print(not(x > 3 and x < 10))

#6
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)
print(x is y)

#7
text = "Hello World"

print("H" in text)
print("hello" in text)
print("z" not in text)

#8
print(6 & 3)
print(6 | 3)
print(6 ^ 3)
