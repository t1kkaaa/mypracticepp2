#1
class Animal:
    def speak(self):
        print("Animal sound")
class Dog(Animal):
    def speak(self):
        print("Woof!")
d=Dog()
d.speak()

#2
class Person:
    def greet(self):
        print("Hello")
class Student(Person):
    def greet(self):
        print("Hi, I'm a student")
s=Student()
s.greet()

#3
class Vehicle:
    def move(self):
        print("Vehicle moves")
class Car(Vehicle):
    def move(self):
        print("Car moves")
c=Car()
c.move()

#4
class Shape:
    def area(self):
        print("Unknown")
class Circle(Shape):
    def area(self):
        print("Area = pi*r^2")
c=Circle()
c.area()

#5
class Bird:
    def fly(self):
        print("Flying")
class Eagle(Bird):
    def fly(self):
        print("Eagle flies high")
e=Eagle()
e.fly()
