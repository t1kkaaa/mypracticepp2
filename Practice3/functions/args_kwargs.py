#1
def sum_numbers(*nums):
    return sum(nums)
print(sum_numbers(1,2,3))

#2
def person_info(**info):
    for key in info:
        print(f"{key} = {info[key]}")
person_info(name="Alice", city="Paris")

#3
def greet_people(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")
greet_people("Hello", "Alice", "Bob")

#4
def show_all(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)
show_all(1,2, name="Alice", age=25)

#5
numbers = [1,2,3,4]
print(sum_numbers(*numbers))
