import math

class Circle:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def circumference(self):
        return 2 * math.pi * self.radius

circle1 = Circle(5, "red")
circle2 = Circle(3.5, "blue")

print("Circle 1:")
print(f"Radius: {circle1.radius}, Color: {circle1.color}")
print(f"Area: {circle1.area():.2f}")
print(f"Circumference: {circle1.circumference():.2f}")

print("\nCircle 2:")
print(f"Radius: {circle2.radius}, Color: {circle2.color}")
print(f"Area: {circle2.area():.2f}")
print(f"Circumference: {circle2.circumference():.2f}")