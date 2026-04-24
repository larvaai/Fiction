"""
============================================================
 10. CÁC KỸ THUẬT HAY DÙNG KHÁC TRONG OOP PYTHON
============================================================
 1. @dataclass      : tự sinh __init__, __repr__, __eq__ cho class dữ liệu
 2. __slots__       : khoá danh sách attribute -> tiết kiệm RAM
 3. Mixin           : class "nhỏ" chỉ cung cấp tính năng cộng thêm
 4. Enum            : kiểu liệt kê
 5. Singleton       : class chỉ có 1 instance duy nhất
 6. Method chaining : return self để nối lệnh
============================================================
"""

# ------------------------------------------------------------
# 1) @dataclass - viết class dữ liệu ngắn gọn
# ------------------------------------------------------------
print("=" * 60)
print("1) @dataclass")
print("=" * 60)

from dataclasses import dataclass, field

@dataclass
class Point:
    x: int
    y: int = 0                         # giá trị mặc định

@dataclass(order=True, frozen=True)    # có sắp xếp và bất biến (immutable)
class Product:
    price: float
    name: str
    tags: list = field(default_factory=list)

p1 = Point(3, 4)
p2 = Point(3, 4)
print(f"p1 = {p1}              <- __repr__ tự sinh")
print(f"p1 == p2 -> {p1 == p2}  <- __eq__ tự sinh")

a = Product(10.0, "bút", ["vp"])
b = Product(5.0, "tẩy")
print(f"sorted: {sorted([a, b])}  <- vì order=True")
try:
    a.price = 20
except Exception as e:
    print(f"Không đổi được (frozen): {type(e).__name__}: {e}")


# ------------------------------------------------------------
# 2) __slots__ - cố định attribute, tiết kiệm RAM
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("2) __slots__")
print("=" * 60)

class LoosePoint:                      # bình thường - có __dict__
    def __init__(self, x, y):
        self.x, self.y = x, y

class TightPoint:
    __slots__ = ("x", "y")             # chỉ cho phép 2 attr này
    def __init__(self, x, y):
        self.x, self.y = x, y

lp = LoosePoint(1, 2)
lp.z = 999                             # OK - thêm attribute lúc chạy được

tp = TightPoint(1, 2)
try:
    tp.z = 999                         # lỗi!
except AttributeError as e:
    print(f"Không thêm attr 'z' vào TightPoint: {e}")

import sys
print(f"LoosePoint có __dict__: {hasattr(lp, '__dict__')}")
print(f"TightPoint có __dict__: {hasattr(tp, '__dict__')} (tiết kiệm RAM)")


# ------------------------------------------------------------
# 3) Mixin - "class nhỏ" gắn thêm tính năng
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("3) Mixin class")
print("=" * 60)

class JSONMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False)

class LoggableMixin:
    def log(self):
        print(f"  [LOG] {type(self).__name__}: {self.__dict__}")

class UserAccount(JSONMixin, LoggableMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email

u = UserAccount("alice", "a@x.com")
u.log()
print(f"  JSON: {u.to_json()}")


# ------------------------------------------------------------
# 4) Enum - kiểu liệt kê
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("4) Enum")
print("=" * 60)

from enum import Enum, auto

class Status(Enum):
    PENDING = auto()
    APPROVED = auto()
    REJECTED = auto()

class Order:
    def __init__(self, id_):
        self.id = id_
        self.status = Status.PENDING
    def approve(self):
        self.status = Status.APPROVED
    def __repr__(self):
        return f"Order#{self.id} [{self.status.name}]"

o = Order(42)
print(o)
o.approve()
print(o)
print(f"So sánh: {o.status == Status.APPROVED}")


# ------------------------------------------------------------
# 5) Singleton - chỉ 1 instance duy nhất (dùng __new__)
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("5) Singleton (dùng __new__)")
print("=" * 60)

class AppConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {}
        return cls._instance

a = AppConfig()
a.settings["lang"] = "vi"

b = AppConfig()                        # KHÔNG tạo mới
print(f"a is b         -> {a is b}")
print(f"b.settings     -> {b.settings}")


# ------------------------------------------------------------
# 6) Method chaining - return self
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("6) Method chaining (fluent interface)")
print("=" * 60)

class QueryBuilder:
    def __init__(self):
        self._parts = []
    def select(self, *cols):
        self._parts.append("SELECT " + ", ".join(cols))
        return self                    # MẤU CHỐT
    def from_(self, table):
        self._parts.append(f"FROM {table}")
        return self
    def where(self, cond):
        self._parts.append(f"WHERE {cond}")
        return self
    def build(self):
        return " ".join(self._parts)

sql = (QueryBuilder()
       .select("id", "name", "email")
       .from_("users")
       .where("age > 18")
       .build())
print(f"  {sql}")
