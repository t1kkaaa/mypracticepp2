#1
square = lambda x: x*x
print(square(5))

#2
add = lambda a,b: a+b
print(add(3,4))

#3
def apply_func(x, func):
    return func(x)
print(apply_func(10, lambda x: x+5))

#4
max_value = lambda a,b: a if a>b else b
print(max_value(7,3))

#5
greet = lambda name: f"Hello, {name}!"
print(greet("Alice"))
