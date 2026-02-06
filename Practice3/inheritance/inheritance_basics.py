#1
class Animal:
    def speak(self):
        print("Some sound")
class Dog(Animal):
    pass
d=Dog()
d.speak()

#2
class Person:
    def greet(self):
        print("Hello")
class Student(Person):
    pass
s=Student()
s.greet()

#3
class Vehicle:
    def move(self):
        print("Moving")
class Car(Vehicle):
    pass
c=Car()
c.move()

#4
class Shape:
    def area(self):
        return 0
class Circle(Shape):
    def __init__(self,r):
        self.r=r
c=Circle(3)
print(c.area())

#5
class Bird:
    def fly(self):
        print("Flying")
class Parrot(Bird):
    pass
p=Parrot()
p.fly()
