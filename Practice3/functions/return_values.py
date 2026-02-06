#1
def square(x):
    return x*x
print(square(5))

#2
def arithmetic(a, b):
    return a+b, a-b, a*b
print(arithmetic(5, 2))

#3
def create_list(n):
    return [i for i in range(n)]
print(create_list(5))

#4
def create_dict():
    return {"name":"Alice", "age":25}
print(create_dict())

#5
def max_of_two(a, b):
    return a if a>b else b
print(max_of_two(3, 7))
