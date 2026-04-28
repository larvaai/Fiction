"""
============================================================
 cingulate.py — Cingulate Cortex hoàn chỉnh (ACC, MCC, PCC)
 Demo: kế thừa đa tầng + polymorphism + @cached_property
============================================================
"""

from functools import cached_property

from .core import BrainModule, MonitorMixin, Signal


# ------------------------------------------------------------
# Lớp trung gian
# ------------------------------------------------------------
class CingulateCortex(BrainModule):
    """Cingulate base — 3 vùng (ACC, MCC, PCC)."""

    def __init__(self, name: str):
        super().__init__(name)
        self._signal_count = 0

    @property
    def label(self) -> str:
        return "CC"

    def process(self, signal: Signal) -> Signal:
        self._signal_count += 1
        return signal


# ------------------------------------------------------------
# 1) ACC — Anterior Cingulate (conflict, error, effort)
# ------------------------------------------------------------
class AnteriorCingulate(CingulateCortex, MonitorMixin):
    """ACC — phát hiện xung đột, lỗi, phân bổ effort."""

    def __init__(self):
        super().__init__("Anterior Cingulate")
        self._conflict_log: list[float] = []

    @property
    def label(self) -> str:
        return "ACC"

    def detect_conflict(
        self, signal_a: Signal, signal_b: Signal
    ) -> float:
        """Hai signal đối lập đều mạnh -> conflict cao."""
        if signal_a >= 0.5 and signal_b >= 0.5:
            conflict = (signal_a.strength + signal_b.strength) / 2
        else:
            conflict = 0.0
        self._conflict_log.append(conflict)
        return conflict

    def detect_error(self, intended: str, actual: str) -> bool:
        """ERN-style: vừa làm sai chưa?"""
        return intended != actual

    def evaluate_effort(self, reward: float, effort: float) -> bool:
        """'Đáng bỏ công không?'"""
        return reward > effort

    def process(self, signal: Signal) -> Signal:
        # Override: ACC khuếch đại signal mới (chú ý đến conflict)
        super().process(signal)
        if signal >= 0.7:
            return signal * 1.1
        return signal


# ------------------------------------------------------------
# 2) MCC — Midcingulate (pain, persistence, foraging)
# ------------------------------------------------------------
class MidCingulate(CingulateCortex):
    """MCC — gắng sức trong khó khăn, tích hợp pain (physical/social)."""

    def __init__(self):
        super().__init__("Midcingulate")
        self._pain_buffer = {"physical": 0.0, "social": 0.0,
                             "emotional": 0.0}

    @property
    def label(self) -> str:
        return "MCC"

    def integrate_pain(
        self, physical: float = 0.0, social: float = 0.0,
        emotional: float = 0.0
    ) -> float:
        """'Đau là đau' bất kể nguồn — MCC hội tụ."""
        self._pain_buffer["physical"] = physical
        self._pain_buffer["social"] = social
        self._pain_buffer["emotional"] = emotional
        return min(1.0, physical + social + emotional)

    def should_persist(
        self, current_reward_rate: float, difficulty: float
    ) -> bool:
        """Persist nếu reward rate còn ổn so với difficulty."""
        return current_reward_rate > difficulty * 0.5


# ------------------------------------------------------------
# 3) PCC — Posterior Cingulate (self-relevance, consciousness gate)
# ------------------------------------------------------------
class PosteriorCingulate(CingulateCortex):
    """PCC — vùng GẮN LIỀN với ý thức nhất."""

    def __init__(self):
        super().__init__("Posterior Cingulate")
        # PCC tham gia DMN -> internal mode khi active cao
        self._consciousness_gate_open = True

    @property
    def label(self) -> str:
        return "PCC"

    @cached_property
    def critical_threshold(self) -> float:
        """Ngưỡng tắt ý thức — tính một lần (cached)."""
        # giả lập tính toán phức tạp (như TMS measurement)
        return 0.15

    def evaluate_self_relevance(self, content: str) -> float:
        """Điều này có liên quan TÔI không?"""
        if not content:
            return 0.0
        keywords = ("tôi", "mình", "bản thân")
        score = sum(0.3 for k in keywords if k in content.lower())
        return min(1.0, score)

    def gate_consciousness(self, activation: float) -> bool:
        """PCC = gateway: tắt -> mất ý thức (anesthesia)."""
        self._consciousness_gate_open = (
            activation >= self.critical_threshold
        )
        return self._consciousness_gate_open

    def process(self, signal: Signal) -> Signal:
        # PCC khuếch đại self-relevant
        super().process(signal)
        relevance = self.evaluate_self_relevance(str(signal.content))
        return signal * (1.0 + relevance)
