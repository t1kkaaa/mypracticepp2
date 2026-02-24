#1
import math
degree = float(input("Input degree: "))
radian = math.radians(degree)

print(f"Output radian: {radian}")

#2
h = float(input("Height: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))

area = ((a + b) / 2) * h

print(f"Expected Output: {area}")

#3
import math
n = int(input("Input number of sides: "))     
s = float(input("Input the length of a side: ")) 

area = (n * s**2) / (4 * math.tan(math.pi / n))

print(f"The area of the polygon is: {area:.0f}")

#4
a = float(input("Length of base: "))
h = float(input("Height of parallelogram: "))

area = a * h

print(f"Expected Output: {area}")