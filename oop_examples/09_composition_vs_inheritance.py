"""
============================================================
 09. COMPOSITION vs AGGREGATION vs ASSOCIATION vs INHERITANCE
============================================================
 Ngoài kế thừa (IS-A), OOP còn các quan hệ khác RẤT quan trọng:

   Inheritance (IS-A)   : Dog IS-A Animal
   Composition (HAS-A, mạnh)
       - Phần tử là thành phần SỐNG CHẾT cùng chủ
       - VD: Engine bên trong Car - huỷ Car thì Engine cũng mất
   Aggregation (HAS-A, yếu)
       - Có quan hệ nhưng phần tử tồn tại độc lập
       - VD: Department "có" Employee, nhưng Employee sống độc lập
   Association (uses-a)
       - Dùng nhau thôi, không sở hữu
       - VD: Driver "lái" Car, nhưng không sở hữu

 NGUYÊN TẮC VÀNG: "Favor composition over inheritance"
============================================================
"""

# ------------------------------------------------------------
# 1) COMPOSITION (mạnh) - Car HAS-A Engine
# ------------------------------------------------------------
print("=" * 60)
print("1) Composition - Car tạo/huỷ cùng Engine")
print("=" * 60)

class Engine:
    def __init__(self, hp):
        self.hp = hp
    def start(self):
        print(f"  Engine {self.hp}HP nổ máy...")

class Car:
    def __init__(self, brand, hp):
        self.brand = brand
        self.engine = Engine(hp)       # engine sinh RA và CHẾT cùng Car
    def drive(self):
        self.engine.start()
        print(f"  {self.brand} chạy đi!")

Car("Toyota", 200).drive()


# ------------------------------------------------------------
# 2) AGGREGATION (yếu) - Department có nhiều Employee (độc lập)
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("2) Aggregation - Employee tồn tại độc lập với Department")
print("=" * 60)

class Employee:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class Department:
    def __init__(self, title):
        self.title = title
        self.members = []              # nhận Employee có sẵn từ ngoài
    def add(self, emp):
        self.members.append(emp)
    def show(self):
        print(f"  Phòng {self.title}: {self.members}")

e1, e2, e3 = Employee("An"), Employee("Bình"), Employee("Chi")
it = Department("IT")
hr = Department("HR")
it.add(e1); it.add(e2)
hr.add(e3); hr.add(e1)                 # An cùng lúc ở 2 phòng - OK

it.show()
hr.show()
print("  (xoá phòng IT thì An, Bình vẫn tồn tại)")


# ------------------------------------------------------------
# 3) ASSOCIATION - Driver dùng Car, không sở hữu
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("3) Association - Driver lái Car")
print("=" * 60)

class Driver:
    def __init__(self, name):
        self.name = name
    def drive(self, car):              # nhận Car bất kỳ làm tham số
        print(f"  {self.name} lái {car.brand}")

car1 = Car("Honda", 150)
car2 = Car("Ford", 250)
alice = Driver("Alice")
alice.drive(car1)
alice.drive(car2)


# ------------------------------------------------------------
# 4) So sánh KẾ THỪA vs COMPOSITION trên cùng bài toán
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("4) CÙNG BÀI TOÁN: máy in đa năng")
print("=" * 60)

# --- Cách A: dùng kế thừa - phình to, cứng, dễ conflict ---
class BasicPrinter:
    def print(self, doc):   print(f"  [Print] {doc}")
class Scanner:
    def scan(self, doc):    print(f"  [Scan] {doc}")
class Fax:
    def fax(self, doc):     print(f"  [Fax] {doc}")

class AllInOne(BasicPrinter, Scanner, Fax):  # đa kế thừa - vấn đề nếu trùng method
    pass

print("  -- Kế thừa:")
m = AllInOne()
m.print("CV"); m.scan("ảnh"); m.fax("hợp đồng")


# --- Cách B: dùng composition - linh hoạt hơn ---
class Machine:
    def __init__(self, **features):
        # features = {"print": BasicPrinter(), "scan": Scanner(), ...}
        self.features = features

    def do(self, action, doc):
        feat = self.features.get(action)
        if feat:
            getattr(feat, action)(doc)
        else:
            print(f"  [X] Máy không có chức năng {action}")

print("  -- Composition (ghép module):")
m2 = Machine(print=BasicPrinter(), scan=Scanner())   # chỉ ghép những gì cần
m2.do("print", "CV")
m2.do("scan", "ảnh")
m2.do("fax", "hợp đồng")                             # không có -> báo lỗi đẹp


# ------------------------------------------------------------
# 5) DELEGATION pattern - object uỷ thác công việc cho object con
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("5) Delegation - TeamLead uỷ việc cho Developer")
print("=" * 60)

class Developer:
    def code(self, feature):
        print(f"  [Dev] code xong: {feature}")

class TeamLead:
    def __init__(self, dev):
        self._dev = dev
    def code(self, feature):              # uỷ thác cho dev
        print("  [Lead] giao việc...")
        self._dev.code(feature)

lead = TeamLead(Developer())
lead.code("login page")
