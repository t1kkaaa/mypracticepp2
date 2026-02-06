#1
class Person:
    def __init__(self, name):
        self.name = name
p = Person("Alice")
print(p.name)

#2
class Dog:
    def __init__(self, breed, age):
        self.breed = breed
        self.age = age
d = Dog("Husky", 3)
print(d.breed, d.age)

#3
class Circle:
    def __init__(self, radius):
        self.radius = radius
c = Circle(5)
print(c.radius)

#4
class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year
car = Car("BMW", 2020)
print(car.model, car.year)

#5
class Book:
    def __init__(self, title):
        self.title = title
b = Book("Python 101")
print(b.title)
