#1
class Person:
    pass
p = Person()

#2
class Dog:
    def bark(self):
        print("Woof!")
d = Dog()
d.bark()

#3
class Cat:
    def meow(self):
        return "Meow!"
c = Cat()
print(c.meow())

#4
class Circle:
    def __init__(self, radius):
        self.radius = radius
c = Circle(5)
print(c.radius)

#5
class Rectangle:
    def area(self, w, h):
        return w*h
r = Rectangle()
print(r.area(3,4))
