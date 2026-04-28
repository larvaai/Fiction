"""
============================================================
 theories.py — 4 LÝ THUYẾT VỀ Ý THỨC
   GWT (Global Workspace), IIT (Integrated Information),
   HOT (Higher-Order Theory), PP (Predictive Processing).

 Demo: ABSTRACTION (ABC) + POLYMORPHISM (mỗi lớp con
       implement cùng interface assess() khác nhau).
       Đồng thời: Duck typing + sort polymorphism.
============================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .core import BrainModule, Signal


# ------------------------------------------------------------
# Abstract base — interface chung cho 4 lý thuyết
# ------------------------------------------------------------
class ConsciousnessTheory(ABC):
    """Mỗi lý thuyết phải trả lời: stimulus này có ý thức không?"""

    name: str = "Abstract"

    @abstractmethod
    def assess(
        self, signal: Signal, modules: list[BrainModule]
    ) -> float:
        """Trả về điểm 'consciousness level' [0, 1]."""

    def is_conscious(
        self, signal: Signal, modules: list[BrainModule]
    ) -> bool:
        return self.assess(signal, modules) >= 0.5

    def __repr__(self):
        return f"{type(self).__name__}({self.name})"

    def __lt__(self, other: "ConsciousnessTheory") -> bool:
        # cho phép sort theo tên — polymorphism
        return self.name < other.name


# ------------------------------------------------------------
# 1) GLOBAL WORKSPACE THEORY (Baars / Dehaene)
# ------------------------------------------------------------
class GWT(ConsciousnessTheory):
    """Ý thức = global ignition + broadcast khắp cortex."""
    name = "Global Workspace Theory"

    IGNITION_THRESHOLD = 0.5

    def assess(self, signal: Signal, modules: list[BrainModule]) -> float:
        if signal < self.IGNITION_THRESHOLD:
            return 0.0   # subliminal — không ignite
        # Broadcast: tỷ lệ module có activation >= 0.3
        active = sum(1 for m in modules if m.activation >= 0.3)
        return min(1.0, active / max(1, len(modules)))


# ------------------------------------------------------------
# 2) INTEGRATED INFORMATION THEORY (Tononi)
# ------------------------------------------------------------
class IIT(ConsciousnessTheory):
    """Ý thức = lượng thông tin tích hợp Φ (phi)."""
    name = "Integrated Information Theory"

    def assess(self, signal: Signal, modules: list[BrainModule]) -> float:
        return self.compute_phi(modules)

    @staticmethod
    def compute_phi(modules: list[BrainModule]) -> float:
        """Φ ≈ tích hợp cross-module.
        Đơn giản hoá: phương sai activation càng nhỏ + số module
        active càng nhiều => integration càng cao."""
        if len(modules) < 2:
            return 0.0
        activations = [m.activation for m in modules]
        n_active = sum(1 for a in activations if a > 0.1)
        if n_active < 2:
            return 0.0
        mean = sum(activations) / len(activations)
        variance = sum((a - mean) ** 2 for a in activations) / len(activations)
        # Φ cao khi nhiều module active VÀ không quá phân hoá
        phi = (n_active / len(modules)) * (1 - min(1.0, variance * 4))
        return max(0.0, min(1.0, phi))


# ------------------------------------------------------------
# 3) HIGHER-ORDER THEORY (Rosenthal / Lau)
# ------------------------------------------------------------
class HOT(ConsciousnessTheory):
    """Ý thức = có representation 'tôi đang xử lý X' ở PFC."""
    name = "Higher-Order Theory"

    def __init__(self, monitor_module: BrainModule):
        self._monitor = monitor_module       # composition: HOT NEEDS PFC

    def assess(self, signal: Signal, modules: list[BrainModule]) -> float:
        """PFC có monitor signal này không?"""
        if self._monitor.activation < 0.3:
            return 0.0       # PFC offline -> dù signal mạnh vẫn không ý thức
        # Signal càng mạnh + monitor càng active -> conscious càng cao
        return min(1.0, signal.strength * self._monitor.activation * 1.2)


# ------------------------------------------------------------
# 4) PREDICTIVE PROCESSING (Friston / Clark / Seth)
# ------------------------------------------------------------
@dataclass
class Prediction:
    expected: str
    confidence: float

    def error_with(self, actual: str) -> float:
        if actual == self.expected:
            return 0.0
        return self.confidence    # tin tưởng càng cao -> sai càng "đau"


class PredictiveProcessing(ConsciousnessTheory):
    """Ý thức = quá trình predict → compare → update liên tục."""
    name = "Predictive Processing"

    def __init__(self):
        self._predictions: list[Prediction] = []
        self._error_history: list[float] = []

    def predict(self, expected: str, confidence: float = 0.7) -> Prediction:
        p = Prediction(expected, confidence)
        self._predictions.append(p)
        return p

    def assess(self, signal: Signal, modules: list[BrainModule]) -> float:
        if not self._predictions:
            return signal.strength * 0.5   # chưa có model -> guess thô
        last = self._predictions[-1]
        actual = str(signal.content)
        error = last.error_with(actual)
        self._error_history.append(error)
        # Surprise (error cao) => ý thức rõ ràng (chú ý)
        # No surprise (error thấp) => habituated, ít ý thức
        return min(1.0, 0.4 + error * 0.6)


# ------------------------------------------------------------
# Aggregator — chạy tất cả lý thuyết, so sánh
# ------------------------------------------------------------
class ConsciousnessAssessor:
    """Tập hợp nhiều theory — dùng polymorphism (duck typing)."""

    def __init__(self, *theories: ConsciousnessTheory):
        self._theories = list(theories)

    def add(self, theory: ConsciousnessTheory) -> "ConsciousnessAssessor":
        self._theories.append(theory)
        return self    # method chaining

    def assess_all(
        self, signal: Signal, modules: list[BrainModule]
    ) -> dict[str, float]:
        # Polymorphism: cùng .assess() nhưng mỗi theory tính khác
        return {
            t.name: round(t.assess(signal, modules), 3)
            for t in self._theories
        }

    def __iter__(self):
        return iter(sorted(self._theories))   # iteration polymorphism

    def __len__(self):
        return len(self._theories)
