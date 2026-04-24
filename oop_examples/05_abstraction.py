"""
============================================================
 TÍNH CHẤT 5: ABSTRACTION (TRỪU TƯỢNG)
 - Giấu chi tiết triển khai, chỉ để lộ "cái gì làm được"
 - Dùng abstract class / abstract method (module abc)
 - Bắt buộc lớp con phải cài đặt
============================================================
"""

from abc import ABC, abstractmethod

# ------------------------------------------------------------
# VÍ DỤ 1 (DỄ): Abstract class cơ bản
# ------------------------------------------------------------
print("=" * 60)
print("VÍ DỤ 1 (DỄ): Shape trừu tượng")
print("=" * 60)

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass      # không cài đặt, bắt buộc con phải override

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2

# Không thể tạo trực tiếp abstract class
try:
    s = Shape()
except TypeError as e:
    print(f"Lỗi khi tạo Shape(): {e}")

sq = Square(4)
ci = Circle(3)
print(f"Square(4).area()  = {sq.area()}")
print(f"Circle(3).area()  = {ci.area()}")


# ------------------------------------------------------------
# VÍ DỤ 2 (TRUNG BÌNH): Abstract với method chung + method bắt buộc
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 2 (TRUNG BÌNH): Employee - tính lương đa hình")
print("=" * 60)

class Employee(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def calculate_salary(self):
        """Mỗi loại nhân viên tính lương khác nhau"""
        pass

    def show(self):                             # method chung không trừu tượng
        print(f"{self.name}: {self.calculate_salary():,} VND")

class FullTime(Employee):
    def __init__(self, name, monthly):
        super().__init__(name)
        self.monthly = monthly
    def calculate_salary(self):
        return self.monthly

class PartTime(Employee):
    def __init__(self, name, hours, rate):
        super().__init__(name)
        self.hours, self.rate = hours, rate
    def calculate_salary(self):
        return self.hours * self.rate

class Freelancer(Employee):
    def __init__(self, name, projects, per_project):
        super().__init__(name)
        self.projects, self.per_project = projects, per_project
    def calculate_salary(self):
        return self.projects * self.per_project

team = [
    FullTime("An",   20_000_000),
    PartTime("Bình", 80, 150_000),
    Freelancer("Cường", 3, 8_000_000),
]
for emp in team:
    emp.show()


# ------------------------------------------------------------
# VÍ DỤ 3 (KHÓ): Abstraction + Template Method Pattern
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 3 (KHÓ): PaymentProcessor - abstract + template method")
print("=" * 60)

class PaymentProcessor(ABC):
    """Template method: định nghĩa khung xử lý chung,
       con chỉ cần cài đặt chi tiết."""

    def process(self, amount):              # template method - KHÔNG abstract
        print(f"\n>>> Bắt đầu xử lý thanh toán {amount:,} VND")
        if not self.validate(amount):
            print("Dừng - không hợp lệ")
            return
        self.authenticate()
        self.pay(amount)
        self.send_receipt(amount)
        print(">>> Hoàn tất\n")

    def validate(self, amount):             # default, con có thể override
        return amount > 0

    def send_receipt(self, amount):         # default
        print(f"[Biên lai] Thanh toán {amount:,} VND thành công")

    @abstractmethod
    def authenticate(self): ...

    @abstractmethod
    def pay(self, amount): ...


class CreditCardPayment(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number
    def authenticate(self):
        print(f"Xác thực thẻ tín dụng ****{self.card_number[-4:]}")
    def pay(self, amount):
        print(f"Trừ {amount:,} VND từ thẻ tín dụng")


class MomoPayment(PaymentProcessor):
    def __init__(self, phone):
        self.phone = phone
    def authenticate(self):
        print(f"Xác thực Momo OTP số {self.phone}")
    def pay(self, amount):
        print(f"Trừ {amount:,} VND từ ví Momo")


class CryptoPayment(PaymentProcessor):
    def __init__(self, wallet):
        self.wallet = wallet
    def validate(self, amount):              # override để thêm điều kiện
        return amount >= 10_000
    def authenticate(self):
        print(f"Ký giao dịch bằng ví {self.wallet[:6]}...")
    def pay(self, amount):
        print(f"Chuyển {amount:,} VND quy đổi sang crypto")
    def send_receipt(self, amount):          # override
        print(f"[On-chain] Hash giao dịch: 0xABC...{amount}")


CreditCardPayment("1234567890123456").process(500_000)
MomoPayment("0909123456").process(200_000)
CryptoPayment("0xDEADBEEF1234").process(5_000)    # dưới 10k -> bị chặn
CryptoPayment("0xDEADBEEF1234").process(1_500_000)
