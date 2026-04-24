"""
============================================================
 TÍNH CHẤT 1: CLASS & OBJECT (LỚP VÀ ĐỐI TƯỢNG)
 - Class: bản thiết kế (blueprint)
 - Object: thực thể cụ thể được tạo từ class
============================================================
"""

# ------------------------------------------------------------
# VÍ DỤ 1 (DỄ): Tạo class đơn giản và đối tượng
# ------------------------------------------------------------
print("=" * 60)
print("VÍ DỤ 1 (DỄ): Class Dog cơ bản")
print("=" * 60)

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} sủa: Gâu gâu!")

dog1 = Dog("Bông", 3)
dog2 = Dog("Milu", 5)

print(f"Chó 1: {dog1.name}, {dog1.age} tuổi")
print(f"Chó 2: {dog2.name}, {dog2.age} tuổi")
dog1.bark()
dog2.bark()


# ------------------------------------------------------------
# VÍ DỤ 2 (TRUNG BÌNH): Class với class variable vs instance variable
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 2 (TRUNG BÌNH): Student - biến lớp vs biến instance")
print("=" * 60)

class Student:
    school = "ĐH Bách Khoa"   # class variable - dùng chung cho tất cả đối tượng
    total_students = 0        # đếm số sinh viên

    def __init__(self, name, gpa):
        self.name = name      # instance variable - riêng của mỗi đối tượng
        self.gpa = gpa
        Student.total_students += 1

    def info(self):
        print(f"SV: {self.name} | GPA: {self.gpa} | Trường: {Student.school}")

s1 = Student("An", 3.5)
s2 = Student("Bình", 3.8)
s3 = Student("Cường", 3.2)

s1.info()
s2.info()
s3.info()
print(f"Tổng số sinh viên đã tạo: {Student.total_students}")


# ------------------------------------------------------------
# VÍ DỤ 3 (KHÓ): Class với classmethod, staticmethod, instance method
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 3 (KHÓ): BankAccount - 3 loại method")
print("=" * 60)

class BankAccount:
    interest_rate = 0.05
    _account_counter = 1000   # đếm số account để sinh id

    def __init__(self, owner, balance=0):
        BankAccount._account_counter += 1
        self.account_id = BankAccount._account_counter
        self.owner = owner
        self.balance = balance

    # instance method: dùng self, thao tác trên đối tượng
    def deposit(self, amount):
        self.balance += amount
        print(f"[{self.account_id}] {self.owner} nạp {amount}. Số dư: {self.balance}")

    # classmethod: dùng cls, thao tác trên class
    @classmethod
    def set_interest_rate(cls, new_rate):
        cls.interest_rate = new_rate
        print(f"Cập nhật lãi suất mới: {cls.interest_rate*100}%")

    # staticmethod: không dùng self/cls, là hàm tiện ích
    @staticmethod
    def is_valid_amount(amount):
        return amount > 0

    def apply_interest(self):
        interest = self.balance * BankAccount.interest_rate
        self.balance += interest
        print(f"[{self.account_id}] {self.owner} nhận lãi {interest:.2f}. Số dư: {self.balance:.2f}")


acc1 = BankAccount("Hùng", 1_000_000)
acc2 = BankAccount("Lan", 5_000_000)

acc1.deposit(500_000)
acc2.deposit(200_000)

print(f"Kiểm tra 100 có hợp lệ? {BankAccount.is_valid_amount(100)}")
print(f"Kiểm tra -50 có hợp lệ? {BankAccount.is_valid_amount(-50)}")

BankAccount.set_interest_rate(0.08)
acc1.apply_interest()
acc2.apply_interest()
