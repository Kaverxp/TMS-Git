class Car:
    def __init__(self, brand, model, color, year):
        self.brand = brand
        self.model = model
        self.color = color
        self.year = year
    
    def get_brand(self):
        return self.brand
    
    def get_model(self):
        return self.model
    
    def get_color(self):
        return self.color
    
    def get_year(self):
        return self.year
    
    def set_brand(self, new_brand):
        self.brand = new_brand
    
    def set_model(self, new_model):
        self.model = new_model
    
    def set_color(self, new_color):
        self.color = new_color
    
    def set_year(self, new_year):
        self.year = new_year

car1 = Car("Toyota", "Camry", "white", 2018)
car2 = Car("BMW", "X5", "black", 2020)
car3 = Car("Tesla", "Model 3", "red", 2022)

cars = [car1, car2, car3]

print("Original cars:")
for i, car in enumerate(cars, 1):
    print(f"Car {i}: {car.get_brand()} {car.get_model()}, {car.get_color()}, {car.get_year()}")

car1.set_color("blue")
car2.set_model("X6")
car3.set_year(2023)

print("\nAfter changes:")
for i, car in enumerate(cars, 1):
    print(f"Car {i}: {car.get_brand()} {car.get_model()}, {car.get_color()}, {car.get_year()}")