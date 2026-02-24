#1
n = int(input("Enter N: "))
squares = (i**2 for i in range(n + 1))

for val in squares:
    print(val)

#2
def even_generator(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield str(i)  

n_input = int(input("Enter n: "))
gen = even_generator(n_input)

print(",".join(gen))

#3
def div_by_3_and_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n_input = int(input("Enter n: "))

for num in div_by_3_and_4(n_input):
    print(num)

#4
a = int(input("Enter start (a): "))
b = int(input("Enter end (b): "))

def squares(start_val, end_val):
    for i in range(start_val, end_val + 1):
        yield i ** 2

print(f"Squares from {a} to {b}:")

for value in squares(a, b):
    print(value)

#5
def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input("Enter n: "))

print(f"Counting down from {n} to 0:")
for num in countdown(n):
    print(num)
