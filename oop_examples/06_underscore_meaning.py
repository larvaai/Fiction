"""
============================================================
 06. Ý NGHĨA CỦA DẤU GẠCH DƯỚI _ TRONG PYTHON OOP
============================================================
 Python có 5 quy ước dùng dấu _ mà lập trình viên OOP phải biết:

 1. _single_leading   : "protected" - quy ước nội bộ (chỉ là convention)
 2. __double_leading  : "private" - Python đổi tên (name mangling)
 3. __double_both__   : "dunder/magic" - Python gọi ngầm (built-in protocol)
 4. single_trailing_  : né trùng từ khóa (class_, type_, id_)
 5. _                 : biến "bỏ đi" / tạm thời
============================================================
"""

print("=" * 60)
print("1. _single_leading  -> PROTECTED (convention)")
print("=" * 60)

class Config:
    def __init__(self):
        self.public_url = "https://api.example.com"   # public
        self._timeout = 30                            # protected - "đừng đụng ngoài class"
        self._retry_count = 3

    def _reload(self):                                # method nội bộ
        print("Đang reload (internal)...")

cfg = Config()
print(f"public_url = {cfg.public_url}")
print(f"_timeout   = {cfg._timeout}   <- KHÔNG bị chặn, chỉ là 'đừng đụng'")
cfg._reload()                                         # chạy được, nhưng KHÔNG nên gọi ngoài class


print("\n" + "=" * 60)
print("2. __double_leading -> PRIVATE (name mangling)")
print("=" * 60)

class Wallet:
    def __init__(self):
        self.__secret = "pin-1234"     # Python sẽ đổi tên thành _Wallet__secret

w = Wallet()
try:
    print(w.__secret)                  # lỗi!
except AttributeError as e:
    print(f"Không truy cập trực tiếp __secret: {e}")

print(f"Nhưng có thể (không nên!): w._Wallet__secret = {w._Wallet__secret}")
print("=> Double underscore dùng để tránh đụng tên khi kế thừa, KHÔNG phải bảo mật thật")


print("\n" + "=" * 60)
print("3. __double_both__ -> DUNDER / MAGIC METHOD")
print("=" * 60)

class Book:
    def __init__(self, title):         # tự chạy khi tạo đối tượng
        self.title = title
    def __str__(self):                 # chạy khi print() hoặc str()
        return f"Sách: {self.title}"
    def __len__(self):                 # chạy khi len()
        return len(self.title)

b = Book("Python 101")
print(b)              # gọi __str__
print(len(b))         # gọi __len__
print("=> dunder được Python gọi ngầm - KHÔNG tự đặt tên kiểu __foo__ cho biến thường")


print("\n" + "=" * 60)
print("4. single_trailing_ -> né trùng keyword")
print("=" * 60)

class Item:
    def __init__(self, name, class_, type_, id_):    # class, type, id đều là keyword/built-in
        self.name = name
        self.class_ = class_
        self.type_ = type_
        self.id_ = id_

it = Item("ring", class_="weapon", type_="rare", id_=101)
print(f"{it.name} | class_={it.class_} | type_={it.type_} | id_={it.id_}")


print("\n" + "=" * 60)
print("5. _ đơn -> biến 'bỏ đi' / tạm")
print("=" * 60)

# Lặp 3 lần, không quan tâm chỉ số
for _ in range(3):
    print("Hello")

# Unpack, chỉ lấy giá trị cần
point = (10, 20, 30)
x, _, z = point
print(f"x={x}, z={z}  (bỏ y)")

# Trong REPL, _ giữ kết quả cuối cùng (không áp dụng trong script)


print("\n" + "=" * 60)
print("TÓM TẮT NHANH")
print("=" * 60)
print("""
    name          : public
    _name         : protected (convention, không chặn)
    __name        : private (name mangling: _Class__name)
    __name__      : dunder - do Python gọi, ĐỪNG tự chế
    name_         : né trùng keyword (class_, type_)
    _             : bỏ qua / tạm
""")
