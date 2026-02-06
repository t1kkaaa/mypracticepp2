#1
class Mother:
    def skills(self):
        print("Cooking")
class Father:
    def skills(self):
        print("Driving")
class Child(Mother,Father):
    pass
c=Child()
c.skills()  # Mother method

#2
class A:
    def a(self):
        print("A")
class B:
    def b(self):
        print("B")
class C(A,B):
    pass
c=C()
c.a()
c.b()

#3
class X:
    def x(self):
        print("X")
class Y:
    def y(self):
        print("Y")
class Z(X,Y):
    pass
z=Z()
z.x()
z.y()

#4
class Engine:
    def start(self):
        print("Engine starts")
class Wheels:
    def roll(self):
        print("Wheels roll")
class Car(Engine,Wheels):
    pass
car=Car()
car.start()
car.roll()

#5
class A:
    def show(self):
        print("A")
class B:
    def show(self):
        print("B")
class C(A,B):
    def show(self):
        super().show()
c=C()
c.show()
