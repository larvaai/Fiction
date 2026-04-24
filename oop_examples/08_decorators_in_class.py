"""
============================================================
 08. DECORATOR TRONG CLASS + __init__ CHUYÊN SÂU
============================================================
 Các decorator CỐT LÕI bạn phải nhớ:

   @staticmethod   : hàm "độc lập", không cần self hay cls
   @classmethod    : nhận cls, thao tác trên class (factory method)
   @property       : biến method thành "thuộc tính đọc"
   @<prop>.setter  : cho phép gán
   @<prop>.deleter : cho phép del

 + __init__ có thể nhận *args, **kwargs, default, keyword-only...
============================================================
"""

# ------------------------------------------------------------
# 1) __init__ - đủ kiểu tham số
# ------------------------------------------------------------
print("=" * 60)
print("1) __init__ nâng cao: default, *args, **kwargs, keyword-only")
print("=" * 60)

class User:
    def __init__(self, name, age=18, *roles, is_active=True, **extra):
        self.name = name
        self.age = age
        self.roles = roles              # tuple
        self.is_active = is_active
        self.extra = extra              # dict

    def show(self):
        print(f"  {self.name} ({self.age}) roles={self.roles} "
              f"active={self.is_active} extra={self.extra}")

User("An").show()
User("Bình", 25, "admin", "editor").show()
User("Chi", 30, "user", is_active=False, email="chi@x.com", city="HN").show()


# ------------------------------------------------------------
# 2) @staticmethod vs @classmethod vs instance method
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("2) 3 loại method")
print("=" * 60)

class Pizza:
    def __init__(self, size, toppings):
        self.size = size
        self.toppings = toppings

    # instance method: thao tác dữ liệu riêng
    def describe(self):
        print(f"  Pizza {self.size} với {self.toppings}")

    # classmethod: trả về đối tượng mới - FACTORY PATTERN
    @classmethod
    def margherita(cls):
        return cls("medium", ["mozzarella", "tomato"])

    @classmethod
    def hawaiian(cls):
        return cls("large", ["ham", "pineapple", "cheese"])

    # staticmethod: hàm tiện ích liên quan đến class nhưng không cần cls
    @staticmethod
    def is_valid_size(size):
        return size in {"small", "medium", "large"}

Pizza.margherita().describe()
Pizza.hawaiian().describe()
print(f"  'xxl' hợp lệ? {Pizza.is_valid_size('xxl')}")
print(f"  'large' hợp lệ? {Pizza.is_valid_size('large')}")


# ------------------------------------------------------------
# 3) @property - getter/setter/deleter
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("3) @property - getter / setter / deleter")
print("=" * 60)

class Celsius:
    def __init__(self, t=0):
        self._t = t

    @property
    def temperature(self):
        print("  (getter chạy)")
        return self._t

    @temperature.setter
    def temperature(self, value):
        print("  (setter chạy)")
        if value < -273.15:
            raise ValueError("< 0 tuyệt đối!")
        self._t = value

    @temperature.deleter
    def temperature(self):
        print("  (deleter chạy)")
        self._t = None

c = Celsius(25)
print(c.temperature)       # gọi getter
c.temperature = 100        # gọi setter
print(c.temperature)
del c.temperature          # gọi deleter
print(c._t)


# ------------------------------------------------------------
# 4) Cached property (tự viết) - chỉ tính 1 lần
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("4) Computed property vs cached_property")
print("=" * 60)

from functools import cached_property

class DataSet:
    def __init__(self, nums):
        self.nums = nums

    @property
    def mean(self):                    # tính mỗi lần truy cập
        print("  (mean - tính lại)")
        return sum(self.nums) / len(self.nums)

    @cached_property
    def total(self):                   # tính 1 lần, lưu lại
        print("  (total - tính 1 lần duy nhất)")
        return sum(self.nums)

ds = DataSet([1, 2, 3, 4, 5])
print(ds.mean); print(ds.mean)         # tính 2 lần
print(ds.total); print(ds.total)       # tính 1 lần


# ------------------------------------------------------------
# 5) Factory method - thay thế overloading constructor
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("5) Factory method: vì Python không có 'overloading constructor'")
print("=" * 60)

class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, s):           # "2026-04-24"
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)

    @classmethod
    def today(cls):
        import datetime
        t = datetime.date.today()
        return cls(t.year, t.month, t.day)

    def __repr__(self):
        return f"Date({self.year}-{self.month:02d}-{self.day:02d})"

print(Date(2026, 4, 24))
print(Date.from_string("2026-12-31"))
print(Date.today())
