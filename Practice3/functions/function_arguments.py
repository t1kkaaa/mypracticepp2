#1
def greet(name="Friend"):
    print(f"Hello, {name}!")
greet()
greet("Bob")

#2
def power(base, exponent):
    return base ** exponent
print(power(2, 3))

#3
def describe_person(name, age):
    print(f"{name} is {age} years old")
describe_person(age=25, name="Alice")

#4
def sum_all(*numbers):
    return sum(numbers)
print(sum_all(1,2,3,4))

#5
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")
print_info(name="Alice", age=25)
