#1
class Person:
    def greet(self):
        print("Hello!")
p = Person()
p.greet()

#2
class Dog:
    def bark(self):
        print("Woof!")
d = Dog()
d.bark()

#3
class Circle:
    def area(self):
        return 3.14*self.radius*self.radius
    def __init__(self,radius):
        self.radius = radius
c = Circle(2)
print(c.area())

#4
class Rectangle:
    def area(self):
        return self.width*self.height
    def __init__(self,w,h):
        self.width=w
        self.height=h
r=Rectangle(3,4)
print(r.area())

#5
class Car:
    def info(self):
        return f"{self.brand} {self.year}"
    def __init__(self, brand, year):
        self.brand=brand
        self.year=year
car=Car("BMW",2020)
print(car.info())
