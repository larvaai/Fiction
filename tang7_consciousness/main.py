"""
============================================================
 main.py — DEMO TOÀN BỘ TẦNG 7

 Chạy:  python3 -m tang7_consciousness.main
============================================================
"""

from .brain import Brain
from .core import (
    BrainModule,
    ConsciousnessState,
    Memory,
    Signal,
    TimeDirection,
)
from .workspace import GlobalWorkspace


def banner(title: str) -> None:
    print("\n" + "=" * 64)
    print(f" {title}")
    print("=" * 64)


def main() -> None:
    # Reset state cho demo lặp được
    GlobalWorkspace.reset()
    BrainModule.reset_count()

    # ----------------------------------------------------------
    banner("1) TẠO SINH VẬT TẦNG 7 (Composition)")
    # ----------------------------------------------------------
    brain = Brain(name="Ellumm-7")
    print(repr(brain))
    print(f"Brain có {len(brain)} module (dùng __len__)")

    # ----------------------------------------------------------
    banner("2) ENCAPSULATION + PROPERTY")
    # ----------------------------------------------------------
    print(f"DMN activation (đọc qua property): {brain.dmn.activation}")
    brain.dmn.activation = 0.7
    print(f"Sau khi set 0.7: {brain.dmn.activation}")
    try:
        brain.dmn.activation = 1.5     # vượt range -> chặn
    except ValueError as e:
        print(f"Validate hoạt động: {e}")

    # ----------------------------------------------------------
    banner("3) OPERATOR OVERLOADING TRÊN SIGNAL")
    # ----------------------------------------------------------
    s1 = Signal("sensory_visual", "thấy quả táo đỏ", strength=0.6)
    s2 = Signal("internal_thought", "tôi đói", strength=0.5)
    print(f"s1 = {s1}")
    print(f"s2 = {s2}")
    print(f"s1 + s2 = {s1 + s2}             # __add__")
    print(f"s1 * 0.5 = {s1 * 0.5}            # __mul__")
    print(f"0.8 * s2 = {0.8 * s2}            # __rmul__")
    print(f"s1 >= 0.5? {s1 >= 0.5}             # __ge__")
    print(f"bool(s1) = {bool(s1)}            # __bool__")

    # ----------------------------------------------------------
    banner("4) POLYMORPHISM — mỗi module process() khác nhau")
    # ----------------------------------------------------------
    self_signal = Signal("internal_self", "tôi đang nghĩ về mình", 0.7)
    print(f"DMN process self-signal: {brain.dmn(self_signal)}")
    print(f"TPN process self-signal: {brain.tpn(self_signal)}")
    print(f"PCC process self-signal: {brain.pcc(self_signal)}")
    print("→ cùng 1 signal, 3 module xử lý 3 kiểu khác nhau")

    # ----------------------------------------------------------
    banner("5) BROADCAST QUA OPERATOR <<")
    # ----------------------------------------------------------
    sig = Signal("sensory_audio", "tiếng động lớn", strength=0.85)
    sig << brain.acc                           # broadcast 1 module
    print(f"ACC sau khi nhận: {brain.acc}")    # __str__
    print(f"ACC is_conscious? {brain.acc.is_conscious}")

    # ----------------------------------------------------------
    banner("6) GLOBAL WORKSPACE — Singleton + Context Manager")
    # ----------------------------------------------------------
    ws1 = GlobalWorkspace()
    ws2 = GlobalWorkspace()
    print(f"ws1 is ws2? {ws1 is ws2}      # singleton")
    with brain.workspace as ws:
        for i, txt in enumerate(["A", "B", "C", "D", "E"]):
            ws.ignite(Signal(f"sensory_{i}", txt, 0.7))
        print(f"Workspace size: {len(ws)} (capacity={ws.CAPACITY})")
        print(f"'A' còn trong workspace? {Signal('s', 'A', 0.5) in ws}")
        print(f"Workspace[-1] = {ws[-1]}      # __getitem__")
        for s in ws:                                  # __iter__
            print(f"   on stage: {s}")

    # ----------------------------------------------------------
    banner("7) PERCEIVE — vòng đời 1 stimulus + 4 LÝ THUYẾT")
    # ----------------------------------------------------------
    # Reset workspace để demo sạch
    GlobalWorkspace.reset()
    brain = Brain(name="Ellumm-7")

    test = Signal("sensory_visual", "có quả táo đỏ trên bàn", 0.85)
    exp = brain.perceive(test)
    print(f"Stimulus: {test}")
    print(f"Conscious? {exp.is_conscious}")
    print("Điểm theo từng lý thuyết:")
    for theory_name, score in exp.theory_scores.items():
        print(f"   {theory_name:35s} = {score}")
    print(f"Modules đạt ý thức: {exp.activated_modules}")

    # ----------------------------------------------------------
    banner("8) ABSTRACTION — không tạo ABC trực tiếp")
    # ----------------------------------------------------------
    from .core import BrainModule as BM
    from .theories import ConsciousnessTheory as CT
    for cls in (BM, CT):
        try:
            cls() if cls is BM else cls()
        except TypeError as e:
            print(f"Không thể tạo {cls.__name__}: {e}")

    # ----------------------------------------------------------
    banner("9) MEMORY (Dataclass frozen) + Mental Time Travel")
    # ----------------------------------------------------------
    brain.remember(Memory(0.8, "đi biển với gia đình", "Đà Nẵng"))
    brain.remember(Memory(-0.6, "bị chó cắn", "công viên"))
    brain.remember(Memory(0.3, "uống cà phê sáng nay", "nhà"))
    print(f"Đã nhớ {brain.memory_count} ký ức")
    print(brain.mental_time_travel(TimeDirection.PAST))
    print(brain.mental_time_travel(TimeDirection.FUTURE, cue="đi học"))
    print(brain.mental_time_travel(TimeDirection.COUNTERFACTUAL))

    # Dataclass frozen không sửa được
    m = Memory(0.5, "test", "ở đâu đó")
    try:
        m.content = "đổi"
    except Exception as e:
        print(f"Memory frozen: {type(e).__name__} - không sửa được")

    # ----------------------------------------------------------
    banner("10) MIND WANDERING (DMN) + ACC conflict + MCC pain")
    # ----------------------------------------------------------
    chain = brain.dmn.mind_wander("đang ngồi yên", steps=4)
    print("Mind wandering:")
    for step in chain:
        print(f"   {step}")

    conflict = brain.acc.detect_conflict(
        Signal("sensory_food", "thèm bánh", 0.8),
        Signal("internal_diet", "đang giảm cân", 0.7),
    )
    print(f"\nACC conflict (food vs diet): {conflict:.2f}")

    pain = brain.mcc.integrate_pain(physical=0.3, social=0.6, emotional=0.2)
    print(f"MCC pain integration (physical+social+emotional): {pain:.2f}")
    print(f"MCC nên persist? {brain.mcc.should_persist(0.4, 0.5)}")

    # ----------------------------------------------------------
    banner("11) METACOGNITION — 'TÔI ĐANG NGHĨ GÌ?'")
    # ----------------------------------------------------------
    report = brain.metacognize()
    for k, v in report.items():
        print(f"   {k:25s}: {v}")

    # ----------------------------------------------------------
    banner("12) STREAM OF CONSCIOUSNESS (iter brain)")
    # ----------------------------------------------------------
    print(f"Số signal trên sân khấu: {len(brain)} module")
    print(f"Workspace có {len(brain.workspace)} signal đang ý thức:")
    for s in brain:                               # __iter__ trên Brain
        print(f"   ★ {s}")

    # ----------------------------------------------------------
    banner("13) TOÀN CẢNH (str(brain))")
    # ----------------------------------------------------------
    print(brain)


if __name__ == "__main__":
    main()
