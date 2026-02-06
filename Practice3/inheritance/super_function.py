#1
class Parent:
    def greet(self):
        print("Hello from Parent")
class Child(Parent):
    def greet(self):
        super().greet()
        print("Hello from Child")
c=Child()
c.greet()

#2
class Animal:
    def __init__(self, name):
        self.name=name
class Dog(Animal):
    def __init__(self,name,breed):
        super().__init__(name)
        self.breed=breed
d=Dog("Rex","Husky")
print(d.name,d.breed)

#3
class Vehicle:
    def start(self):
        print("Vehicle starting")
class Car(Vehicle):
    def start(self):
        super().start()
        print("Car starting")
c=Car()
c.start()

#4
class Shape:
    def __init__(self, color):
        self.color=color
class Circle(Shape):
    def __init__(self,radius,color):
        super().__init__(color)
        self.radius=radius
c=Circle(5,"Red")
print(c.radius,c.color)

#5
class A:
    def show(self):
        print("A")
class B(A):
    def show(self):
        super().show()
        print("B")
b=B()
b.show()
