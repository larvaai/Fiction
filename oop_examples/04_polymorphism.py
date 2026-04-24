"""
============================================================
 TÍNH CHẤT 4: POLYMORPHISM (ĐA HÌNH)
 - Cùng 1 "giao diện" nhưng hành vi khác nhau theo từng class
 - Method Overriding: ghi đè method của cha
 - Duck Typing: nếu "kêu như vịt, đi như vịt" thì là vịt
 - Operator Overloading: nạp chồng toán tử
============================================================
"""

# ------------------------------------------------------------
# VÍ DỤ 1 (DỄ): Method Overriding
# ------------------------------------------------------------
print("=" * 60)
print("VÍ DỤ 1 (DỄ): Method overriding - speak()")
print("=" * 60)

class Animal:
    def speak(self):
        print("Một loài động vật kêu gì đó")

class Dog(Animal):
    def speak(self):                     # ghi đè
        print("Chó: Gâu gâu!")

class Cat(Animal):
    def speak(self):
        print("Mèo: Meo meo!")

class Cow(Animal):
    def speak(self):
        print("Bò: Ò ò ò!")

# Dùng chung 1 vòng lặp - cùng 1 lời gọi, hành vi khác nhau
animals = [Dog(), Cat(), Cow(), Animal()]
for a in animals:
    a.speak()


# ------------------------------------------------------------
# VÍ DỤ 2 (TRUNG BÌNH): Duck Typing + đa hình qua interface
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 2 (TRUNG BÌNH): Duck Typing - tính diện tích")
print("=" * 60)

class Circle:
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2

class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

class Triangle:
    def __init__(self, base, height):
        self.base, self.height = base, height
    def area(self):
        return 0.5 * self.base * self.height

# Không cần kế thừa chung, chỉ cần có method area() là "đa hình" được
def print_total_area(shapes):
    total = 0
    for s in shapes:
        a = s.area()     # cùng 1 lời gọi, nhiều cách tính khác nhau
        print(f"{type(s).__name__:10s} diện tích = {a}")
        total += a
    print(f"Tổng diện tích = {total}")

print_total_area([Circle(3), Rectangle(4, 5), Triangle(6, 7)])


# ------------------------------------------------------------
# VÍ DỤ 3 (KHÓ): Operator Overloading - nạp chồng toán tử
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 3 (KHÓ): Vector - nạp chồng +, -, *, ==, str()")
print("=" * 60)

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):        # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):        # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):       # v1 * 3  (scalar)
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):         # v1 == v2
        return self.x == other.x and self.y == other.y

    def __len__(self):               # len(v) - độ dài làm tròn
        return int((self.x**2 + self.y**2) ** 0.5)

    def __str__(self):               # str(v), print(v)
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

v1 = Vector(2, 3)
v2 = Vector(5, 7)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v2 - v1 = {v2 - v1}")
print(f"v1 * 3  = {v1 * 3}")
print(f"v1 == Vector(2,3)? {v1 == Vector(2,3)}")
print(f"v1 == v2?          {v1 == v2}")
print(f"len(v2) = {len(v2)}  (căn(25+49) ≈ 8)")


# ------------------------------------------------------------
# BONUS: Đa hình với hàm built-in - len()
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("BONUS: len() là đa hình sẵn có trong Python")
print("=" * 60)
print(f"len('hello')      = {len('hello')}")
print(f"len([1,2,3,4])    = {len([1,2,3,4])}")
print(f"len({{'a':1,'b':2}}) = {len({'a':1,'b':2})}")
print(f"len(Vector(3,4))  = {len(Vector(3,4))}")
