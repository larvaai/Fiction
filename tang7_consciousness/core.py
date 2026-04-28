"""
============================================================
 core.py — NỀN TẢNG
   * Abstraction:   BrainModule (ABC)
   * Encapsulation: __private, _protected, @property
   * Polymorphism:  Signal (operator overload)
   * Mixins:        SelfReferenceMixin, BroadcastMixin, MonitorMixin
   * Enum:          ConsciousnessState, NetworkMode, TimeDirection
   * Dataclass:     Memory (frozen)
   * __slots__:     Signal (tiết kiệm RAM)
============================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any


# ============================================================
# 1) ENUMS — các kiểu liệt kê dùng khắp project
# ============================================================
class ConsciousnessState(Enum):
    AWAKE = auto()
    DREAMING = auto()         # REM
    DEEP_SLEEP = auto()       # NREM SWS
    ANESTHESIA = auto()
    FLOW = auto()
    MEDITATION = auto()
    LUCID_DREAMING = auto()


class NetworkMode(Enum):
    EXTERNAL = "TPN dominant - looking OUT"
    INTERNAL = "DMN dominant - looking IN"
    SWITCHING = "SN active - chuyển mode"


class TimeDirection(Enum):
    PAST = "retrospection"
    FUTURE = "prospection"
    COUNTERFACTUAL = "what_if"


# ============================================================
# 2) DATACLASS — Memory bất biến (frozen=True)
# ============================================================
@dataclass(frozen=True, order=True)
class Memory:
    """Ký ức episodic - immutable, có thể sort, hashable."""
    emotional_tag: float                     # đặt đầu để sort theo cảm xúc
    content: str = field(compare=False)
    spatial_context: str = field(default="", compare=False)
    timestamp: datetime = field(
        default_factory=datetime.now, compare=False
    )

    def __post_init__(self):
        # frozen vẫn validate được qua __post_init__
        if not -1.0 <= self.emotional_tag <= 1.0:
            raise ValueError(
                f"emotional_tag phải trong [-1, 1], nhận {self.emotional_tag}"
            )


# ============================================================
# 3) SIGNAL — Operator Overloading + __slots__
# ============================================================
class Signal:
    """Tín hiệu thần kinh — demo nạp chồng toán tử."""
    __slots__ = ("source", "content", "strength", "timestamp")

    def __init__(self, source: str, content: Any, strength: float = 0.5):
        self.source = source
        self.content = content
        # encapsulation: clamp về [0, 1]
        self.strength = max(0.0, min(1.0, strength))
        self.timestamp = datetime.now()

    # ---- Operator overloading ----
    def __add__(self, other: "Signal") -> "Signal":
        """signal + signal -> tín hiệu kết hợp (giới hạn 1.0)."""
        return Signal(
            source=f"{self.source}+{other.source}",
            content=(self.content, other.content),
            strength=min(1.0, self.strength + other.strength),
        )

    def __mul__(self, factor: float) -> "Signal":
        """signal * factor -> điều chỉnh cường độ (gain)."""
        return Signal(self.source, self.content, self.strength * factor)

    __rmul__ = __mul__   # cho phép 0.5 * signal

    def __lshift__(self, target):
        """signal << module — broadcast theo phong cách GWT."""
        return target.receive(self)

    def __ge__(self, threshold: float) -> bool:
        return self.strength >= threshold

    def __lt__(self, threshold: float) -> bool:
        return self.strength < threshold

    def __bool__(self) -> bool:
        """if signal: -> True khi cường độ > 0."""
        return self.strength > 0.0

    def __repr__(self):
        return (
            f"Signal(src={self.source!r}, "
            f"strength={self.strength:.2f})"
        )


# ============================================================
# 4) ABSTRACT BASE CLASS — BrainModule
#    Đỉnh của hierarchy. Mọi vùng não kế thừa.
# ============================================================
class BrainModule(ABC):
    """Abstract base — không thể tạo trực tiếp."""

    _instance_count = 0          # class variable đếm số module đã tạo
    THRESHOLD_CONSCIOUS = 0.5    # Dehaene's ignition threshold

    def __init__(self, name: str):
        BrainModule._instance_count += 1
        self._id = BrainModule._instance_count
        self._name = name
        self._activation = 0.0                  # protected
        self.__connections: list = []           # private (name mangling)
        self.__history: list = []               # private

    # ---- Bắt buộc override ở lớp con ----
    @abstractmethod
    def process(self, signal: Signal) -> Signal:
        """Mỗi module xử lý signal khác nhau (polymorphism)."""

    @property
    @abstractmethod
    def label(self) -> str:
        """Nhãn ngắn gọn cho module (vd 'DMN', 'ACC')."""

    # ---- Concrete methods (kế thừa được dùng luôn) ----
    def connect(self, other: "BrainModule") -> "BrainModule":
        """Method chaining: a.connect(b).connect(c).connect(d)"""
        self.__connections.append(other)
        return self

    def receive(self, signal: Signal) -> Signal:
        """Đầu vào - chạy process() và lưu lịch sử."""
        self._activation = signal.strength
        self.__history.append((signal.timestamp, signal.strength))
        return self.process(signal)

    # ---- Encapsulation: @property + setter có validate ----
    @property
    def activation(self) -> float:
        return self._activation

    @activation.setter
    def activation(self, value: float) -> None:
        if not 0.0 <= value <= 1.0:
            raise ValueError("activation phải trong [0, 1]")
        self._activation = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_conscious(self) -> bool:
        """Module có 'lên sân khấu' (GWT) chưa?"""
        return self._activation >= self.THRESHOLD_CONSCIOUS

    @property
    def history_size(self) -> int:
        return len(self.__history)   # truy cập private trong class - OK

    # ---- classmethod ----
    @classmethod
    def reset_count(cls) -> None:
        cls._instance_count = 0

    # ---- staticmethod (hàm tiện ích, không cần self/cls) ----
    @staticmethod
    def is_subliminal(signal: Signal) -> bool:
        """Signal dưới ngưỡng ý thức (subliminal stimulus)."""
        return signal.strength < BrainModule.THRESHOLD_CONSCIOUS

    # ---- Dunder methods ----
    def __call__(self, signal: Signal) -> Signal:
        """module(signal) — gọi như hàm."""
        return self.receive(signal)

    def __len__(self) -> int:
        """len(module) — số kết nối."""
        return len(self.__connections)

    def __lt__(self, other: "BrainModule") -> bool:
        """sort modules theo activation."""
        return self._activation < other._activation

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BrainModule) and self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self._name!r}, "
            f"act={self._activation:.2f})"
        )

    def __str__(self) -> str:
        marker = "★" if self.is_conscious else "·"
        return f"{marker} [{self.label}] {self._name} ({self._activation:.2f})"


# ============================================================
# 5) MIXINS — class nhỏ chỉ thêm 1 tính năng
# ============================================================
class SelfReferenceMixin:
    """Khả năng nhận biết stimulus có liên quan đến BẢN THÂN."""

    SELF_KEYWORDS = ("tôi", "mình", "bản thân", " i ", " me ", " my ")

    def is_about_self(self, signal: Signal) -> bool:
        text = str(signal.content).lower()
        return any(k in f" {text} " for k in self.SELF_KEYWORDS)


class BroadcastMixin:
    """Khả năng broadcast signal đến nhiều module (GWT-style)."""

    def broadcast_to(self, modules: list, signal: Signal) -> dict:
        results = {}
        for m in modules:
            results[m.name] = (signal << m).strength    # dùng <<
        return results


class MonitorMixin:
    """Khả năng giám sát module khác (HOT-style higher-order)."""

    def monitor(self, target: BrainModule) -> dict:
        return {
            "target": target.name,
            "activation": target.activation,
            "is_conscious": target.is_conscious,
        }
