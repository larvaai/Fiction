"""
============================================================
 TÍNH CHẤT 3: INHERITANCE (KẾ THỪA)
 - Class con thừa hưởng thuộc tính/phương thức của class cha
 - Dùng super() để gọi code của cha
 - Có nhiều kiểu: single, multi-level, multiple, hierarchical
============================================================
"""

# ------------------------------------------------------------
# VÍ DỤ 1 (DỄ): Kế thừa đơn (single inheritance)
# ------------------------------------------------------------
print("=" * 60)
print("VÍ DỤ 1 (DỄ): Animal -> Dog")
print("=" * 60)

class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} đang ăn")

    def sleep(self):
        print(f"{self.name} đang ngủ")

class Dog(Animal):                  # Dog kế thừa Animal
    def bark(self):
        print(f"{self.name}: Gâu gâu!")

d = Dog("Bông")
d.eat()      # kế thừa từ Animal
d.sleep()    # kế thừa từ Animal
d.bark()     # riêng của Dog


# ------------------------------------------------------------
# VÍ DỤ 2 (TRUNG BÌNH): Kế thừa nhiều tầng + super()
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 2 (TRUNG BÌNH): Vehicle -> Car -> ElectricCar (multi-level)")
print("=" * 60)

class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed
        print(f"[Vehicle.__init__] {brand} được khởi tạo")

    def run(self):
        print(f"{self.brand} chạy với tốc độ {self.speed} km/h")

class Car(Vehicle):
    def __init__(self, brand, speed, num_wheels):
        super().__init__(brand, speed)       # gọi init của cha
        self.num_wheels = num_wheels
        print(f"[Car.__init__] Xe có {num_wheels} bánh")

    def honk(self):
        print(f"{self.brand}: Beep beep!")

class ElectricCar(Car):
    def __init__(self, brand, speed, num_wheels, battery_kwh):
        super().__init__(brand, speed, num_wheels)
        self.battery_kwh = battery_kwh
        print(f"[ElectricCar.__init__] Pin {battery_kwh} kWh")

    def charge(self):
        print(f"{self.brand} đang sạc... dung lượng {self.battery_kwh} kWh")

tesla = ElectricCar("Tesla Model 3", 250, 4, 75)
print("---")
tesla.run()     # từ Vehicle
tesla.honk()    # từ Car
tesla.charge()  # của chính nó


# ------------------------------------------------------------
# VÍ DỤ 3 (KHÓ): Đa kế thừa (multiple inheritance) + MRO
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 3 (KHÓ): Multiple inheritance - MRO (Method Resolution Order)")
print("=" * 60)

class Flyable:
    def move(self):
        print("Bay lượn trên trời")

    def describe(self):
        print("Tôi biết bay")

class Swimmable:
    def move(self):
        print("Bơi dưới nước")

    def describe(self):
        print("Tôi biết bơi")

class Duck(Flyable, Swimmable):       # đa kế thừa
    def describe(self):
        print("Tôi là vịt!")
        super().describe()             # gọi describe theo MRO
        # Gọi rõ ràng từng lớp cha:
        Flyable.describe(self)
        Swimmable.describe(self)

d = Duck()
d.move()             # theo MRO, lấy của Flyable trước
d.describe()

print(f"\nThứ tự MRO của Duck: {[c.__name__ for c in Duck.__mro__]}")


# ------------------------------------------------------------
# BONUS: Kiểm tra quan hệ kế thừa với isinstance / issubclass
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("BONUS: isinstance & issubclass")
print("=" * 60)
print(f"tesla là ElectricCar? {isinstance(tesla, ElectricCar)}")
print(f"tesla là Car?         {isinstance(tesla, Car)}")
print(f"tesla là Vehicle?     {isinstance(tesla, Vehicle)}")
print(f"ElectricCar kế thừa Vehicle? {issubclass(ElectricCar, Vehicle)}")
