"""
============================================================
 TÍNH CHẤT 2: ENCAPSULATION (ĐÓNG GÓI)
 - Giấu dữ liệu bên trong class
 - Truy cập qua getter/setter hoặc property
 - 3 mức: public, _protected, __private
============================================================
"""

# ------------------------------------------------------------
# VÍ DỤ 1 (DỄ): Public vs Private
# ------------------------------------------------------------
print("=" * 60)
print("VÍ DỤ 1 (DỄ): Person - public và private")
print("=" * 60)

class Person:
    def __init__(self, name, age):
        self.name = name          # public
        self.__age = age          # private (name mangling)

    def get_age(self):
        return self.__age

    def set_age(self, new_age):
        if new_age >= 0:
            self.__age = new_age
        else:
            print("Tuổi không hợp lệ!")

p = Person("Minh", 25)
print(f"Tên (public): {p.name}")
print(f"Tuổi (qua getter): {p.get_age()}")

p.set_age(30)
print(f"Sau khi set 30: {p.get_age()}")

p.set_age(-5)          # bị chặn
print(f"Sau khi set -5: {p.get_age()}")

# Truy cập trực tiếp __age sẽ lỗi
try:
    print(p.__age)
except AttributeError as e:
    print(f"Lỗi khi truy cập __age trực tiếp: {e}")


# ------------------------------------------------------------
# VÍ DỤ 2 (TRUNG BÌNH): Dùng @property để thanh lịch hơn
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 2 (TRUNG BÌNH): Temperature - property getter/setter")
print("=" * 60)

class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Không thể thấp hơn 0 tuyệt đối!")
        self._celsius = value

    @property
    def fahrenheit(self):          # chỉ đọc - computed property
        return self._celsius * 9/5 + 32

t = Temperature(25)
print(f"Celsius: {t.celsius}°C")
print(f"Fahrenheit (tự tính): {t.fahrenheit}°F")

t.celsius = 100
print(f"Đổi sang 100°C -> {t.fahrenheit}°F")

try:
    t.celsius = -300
except ValueError as e:
    print(f"Lỗi: {e}")


# ------------------------------------------------------------
# VÍ DỤ 3 (KHÓ): Đóng gói thực sự - BankVault với validation
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("VÍ DỤ 3 (KHÓ): BankVault - đóng gói hoàn chỉnh")
print("=" * 60)

class BankVault:
    def __init__(self, owner, pin):
        self.owner = owner
        self.__pin = pin            # private
        self.__balance = 0          # private
        self.__transaction_log = [] # private

    def __check_pin(self, pin):     # private method
        return pin == self.__pin

    def deposit(self, amount, pin):
        if not self.__check_pin(pin):
            print("Sai PIN - từ chối nạp tiền!")
            return
        if amount <= 0:
            print("Số tiền không hợp lệ!")
            return
        self.__balance += amount
        self.__transaction_log.append(f"+{amount}")
        print(f"Nạp {amount} thành công")

    def withdraw(self, amount, pin):
        if not self.__check_pin(pin):
            print("Sai PIN - từ chối rút tiền!")
            return
        if amount > self.__balance:
            print("Không đủ tiền!")
            return
        self.__balance -= amount
        self.__transaction_log.append(f"-{amount}")
        print(f"Rút {amount} thành công")

    def get_balance(self, pin):
        if not self.__check_pin(pin):
            print("Sai PIN!")
            return None
        return self.__balance

    def get_history(self, pin):
        if not self.__check_pin(pin):
            print("Sai PIN!")
            return None
        return list(self.__transaction_log)  # trả bản copy


vault = BankVault("Hoa", pin=1234)
vault.deposit(1_000_000, pin=1234)
vault.deposit(500_000, pin=9999)     # sai pin
vault.withdraw(300_000, pin=1234)
vault.withdraw(10_000_000, pin=1234) # không đủ
print(f"Số dư: {vault.get_balance(1234)}")
print(f"Lịch sử: {vault.get_history(1234)}")

# Bên ngoài không thể "sửa" số dư trực tiếp
print(f"Truy cập _BankVault__balance (hack): {vault._BankVault__balance}")
print("(Python dùng 'name mangling' chứ không khóa cứng, nhưng quy ước là không đụng vào)")
