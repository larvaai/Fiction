"""
============================================================
 07. DUNDER / MAGIC METHODS - CÁC HÀM __xxx__ HAY DÙNG
============================================================
 Nhóm 1: Khởi tạo & huỷ
     __new__   : tạo object (ít dùng, dành cho metaclass/singleton)
     __init__  : khởi tạo (constructor) - HAY DÙNG NHẤT
     __del__   : destructor - khi object bị xoá

 Nhóm 2: Biểu diễn
     __str__   : str(obj), print(obj) - cho người đọc
     __repr__  : repr(obj), debug - cho dev đọc
     __format__: f"{obj:spec}"

 Nhóm 3: So sánh
     __eq__  __ne__  __lt__  __le__  __gt__  __ge__
     __hash__   (để dùng trong set/dict key)

 Nhóm 4: Container (giả làm list/dict)
     __len__  __getitem__  __setitem__  __delitem__  __contains__
     __iter__  __next__     (giả làm iterator)

 Nhóm 5: Toán tử
     __add__  __sub__  __mul__  __truediv__  __floordiv__  __mod__
     __neg__  __abs__  __pow__

 Nhóm 6: Callable & context manager
     __call__          : obj() gọi được như hàm
     __enter__  __exit__ : dùng với "with"

 Nhóm 7: Thuộc tính động
     __getattr__  __setattr__  __delattr__
============================================================
"""

# ------------------------------------------------------------
# 1) __init__, __del__, __new__
# ------------------------------------------------------------
print("=" * 60)
print("NHÓM 1: Khởi tạo & huỷ")
print("=" * 60)

class File:
    def __new__(cls, *a, **kw):
        print("  __new__ : cấp phát vùng nhớ cho object")
        return super().__new__(cls)

    def __init__(self, name):
        print(f"  __init__: khởi tạo với tên = {name}")
        self.name = name

    def __del__(self):
        print(f"  __del__ : huỷ file {self.name}")

f = File("data.txt")
del f


# ------------------------------------------------------------
# 2) __str__ vs __repr__
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 2: __str__ vs __repr__")
print("=" * 60)

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self):
        return f"({self.x}, {self.y})"                # người đọc
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"       # dev đọc / debug
    def __format__(self, spec):
        if spec == "polar":
            r = (self.x**2 + self.y**2) ** 0.5
            return f"r={r:.2f}"
        return str(self)

p = Point(3, 4)
print(f"print(p)     -> {p}")            # dùng __str__
print(f"repr(p)      -> {repr(p)}")      # dùng __repr__
print(f"f'{{p}}'       -> {p}")
print(f"f'{{p:polar}}' -> {p:polar}")    # dùng __format__
print(f"[p, p, p]    -> {[p, p, p]}")    # list in các phần tử bằng __repr__


# ------------------------------------------------------------
# 3) So sánh + hash
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 3: So sánh & hash")
print("=" * 60)

class Money:
    def __init__(self, amount):
        self.amount = amount
    def __eq__(self, other):  return self.amount == other.amount
    def __lt__(self, other):  return self.amount <  other.amount
    def __le__(self, other):  return self.amount <= other.amount
    def __hash__(self):       return hash(self.amount)     # cần có để vào set/dict
    def __repr__(self):       return f"${self.amount}"

a, b, c = Money(100), Money(200), Money(100)
print(f"a == c: {a == c}")
print(f"a < b : {a < b}")
print(f"sorted: {sorted([b, a, c])}")
print(f"set   : {set([a, b, c])}   (a==c nên bị gộp)")


# ------------------------------------------------------------
# 4) Container protocol: __len__, __getitem__, __iter__, __contains__
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 4: Container - giả làm list")
print("=" * 60)

class Playlist:
    def __init__(self, songs):
        self._songs = list(songs)
    def __len__(self):           return len(self._songs)
    def __getitem__(self, i):    return self._songs[i]
    def __setitem__(self, i, v): self._songs[i] = v
    def __delitem__(self, i):    del self._songs[i]
    def __contains__(self, v):   return v in self._songs
    def __iter__(self):          return iter(self._songs)

pl = Playlist(["song A", "song B", "song C"])
print(f"len         = {len(pl)}")
print(f"pl[0]       = {pl[0]}")
print(f"'song B' in = {'song B' in pl}")
pl[1] = "song B - remix"
del pl[2]
for s in pl:
    print(f"  - {s}")


# ------------------------------------------------------------
# 5) Iterator riêng
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 4b: Iterator với __iter__ + __next__")
print("=" * 60)

class CountDown:
    def __init__(self, start):
        self.n = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for v in CountDown(5):
    print(v, end=" ")
print()


# ------------------------------------------------------------
# 6) Toán tử
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 5: Nạp chồng toán tử")
print("=" * 60)

class Money2:
    def __init__(self, amount):
        self.amount = amount
    def __add__(self, other):   return Money2(self.amount + other.amount)
    def __sub__(self, other):   return Money2(self.amount - other.amount)
    def __mul__(self, n):       return Money2(self.amount * n)          # M * 3
    def __rmul__(self, n):      return Money2(self.amount * n)          # 3 * M
    def __neg__(self):          return Money2(-self.amount)
    def __abs__(self):          return Money2(abs(self.amount))
    def __repr__(self):         return f"${self.amount}"

m1, m2 = Money2(100), Money2(30)
print(f"m1 + m2 = {m1 + m2}")
print(f"m1 - m2 = {m1 - m2}")
print(f"m1 * 3  = {m1 * 3}")
print(f"3 * m1  = {3 * m1}    (dùng __rmul__)")
print(f"-m1     = {-m1}")
print(f"abs(-m1)= {abs(-m1)}")


# ------------------------------------------------------------
# 7) __call__ - object như một hàm
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 6a: __call__ - object 'callable'")
print("=" * 60)

class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)
print(f"double(5) = {double(5)}   <- gọi như hàm")
print(f"triple(5) = {triple(5)}")
print(f"callable(double) = {callable(double)}")


# ------------------------------------------------------------
# 8) Context manager: __enter__ __exit__
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 6b: __enter__/__exit__ - dùng với 'with'")
print("=" * 60)

class Timer:
    def __enter__(self):
        import time
        self.t0 = time.time()
        print("  [Timer] bắt đầu")
        return self
    def __exit__(self, exc_type, exc, tb):
        import time
        print(f"  [Timer] kết thúc, {time.time()-self.t0:.4f}s")
        return False   # False nghĩa là KHÔNG nuốt exception

with Timer() as t:
    total = sum(range(1_000_000))
print(f"total = {total}")


# ------------------------------------------------------------
# 9) __getattr__ / __setattr__ - thuộc tính động
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("NHÓM 7: Attribute động")
print("=" * 60)

class LazyDict:
    def __init__(self):
        self._data = {}
    def __getattr__(self, name):      # chỉ gọi khi KHÔNG tìm thấy attr bình thường
        return self._data.get(name, f"<không có {name}>")
    def __setattr__(self, name, value):
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value

ld = LazyDict()
ld.username = "alice"
ld.level = 99
print(f"ld.username = {ld.username}")
print(f"ld.level    = {ld.level}")
print(f"ld.missing  = {ld.missing}")    # không lỗi, trả về fallback
