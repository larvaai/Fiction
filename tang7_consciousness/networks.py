"""
============================================================
 networks.py — DMN, TPN, SN
 Demo: INHERITANCE (single, multi-level, multiple)
       + Polymorphism (override process), Composition.
============================================================

 Hierarchy:
     BrainModule (abstract)              [core.py]
         └── Network (abstract trung gian)
                ├── DefaultModeNetwork (+ SelfReferenceMixin)  ← multiple
                ├── TaskPositiveNetwork
                └── SalienceNetwork (+ BroadcastMixin)         ← multiple
============================================================
"""

import random

from .core import (
    BrainModule,
    BroadcastMixin,
    NetworkMode,
    SelfReferenceMixin,
    Signal,
)


# ------------------------------------------------------------
# 1) Network — abstract trung gian (multi-level inheritance)
# ------------------------------------------------------------
class Network(BrainModule):
    """Lớp trung gian: 1 mạng não chứa nhiều node."""

    def __init__(self, name: str):
        super().__init__(name)
        self._nodes: list[BrainModule] = []   # composition / aggregation
        self._mode = NetworkMode.EXTERNAL

    def add_node(self, node: BrainModule) -> "Network":
        """Method chaining: net.add_node(a).add_node(b)..."""
        self._nodes.append(node)
        return self

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def mode(self) -> NetworkMode:
        return self._mode

    # vẫn abstract (label, process) — buộc con implement
    def process(self, signal: Signal) -> Signal:
        # Default: forward qua tất cả node, gain trung bình
        if not self._nodes:
            return signal
        result = signal
        for node in self._nodes:
            result = node(result)
        return result


# ------------------------------------------------------------
# 2) DEFAULT MODE NETWORK — Multiple inheritance
# ------------------------------------------------------------
class DefaultModeNetwork(Network, SelfReferenceMixin):
    """DMN — internal mentation, mind wandering, self, mental time travel."""

    AMPLIFY_SELF = 1.4    # tăng signal liên quan đến bản thân
    SUPPRESS_EXTERNAL = 0.6

    def __init__(self):
        super().__init__("Default Mode Network")
        self._mode = NetworkMode.INTERNAL
        self._wandering_chain: list[str] = []

    @property
    def label(self) -> str:
        return "DMN"

    def process(self, signal: Signal) -> Signal:
        """Override: DMN ưu tiên self-relevant, ức chế external."""
        self._wandering_chain.append(str(signal.content)[:30])
        if self.is_about_self(signal):       # method từ mixin
            return signal * self.AMPLIFY_SELF
        return signal * self.SUPPRESS_EXTERNAL

    def mind_wander(self, seed: str, steps: int = 5) -> list[str]:
        """Sinh chuỗi mind wandering — daydream, mental simulation."""
        topics = ["bản thân", "tương lai", "quá khứ",
                  "người khác", "ý nghĩa", "kỷ niệm"]
        chain = [seed]
        for _ in range(steps):
            chain.append(f"{chain[-1]} → {random.choice(topics)}")
        return chain


# ------------------------------------------------------------
# 3) TASK POSITIVE NETWORK — single inheritance
# ------------------------------------------------------------
class TaskPositiveNetwork(Network):
    """TPN — focused external attention, problem solving."""

    AMPLIFY_EXTERNAL = 1.4
    SUPPRESS_INTERNAL = 0.5

    def __init__(self):
        super().__init__("Task Positive Network")
        self._mode = NetworkMode.EXTERNAL
        self._current_task: str | None = None

    @property
    def label(self) -> str:
        return "TPN"

    def set_task(self, task: str) -> "TaskPositiveNetwork":
        self._current_task = task
        return self

    def process(self, signal: Signal) -> Signal:
        """Override: TPN khuếch đại external, ức chế internal."""
        if signal.source.startswith("sensory_"):
            return signal * self.AMPLIFY_EXTERNAL
        if signal.source.startswith("internal_"):
            return signal * self.SUPPRESS_INTERNAL
        return signal


# ------------------------------------------------------------
# 4) SALIENCE NETWORK — Multiple inheritance + Composition
# ------------------------------------------------------------
class SalienceNetwork(Network, BroadcastMixin):
    """SN — switch giữa DMN và TPN. Composition: HAS-A DMN, HAS-A TPN."""

    SWITCH_THRESHOLD = 0.6

    def __init__(self, dmn: DefaultModeNetwork, tpn: TaskPositiveNetwork):
        super().__init__("Salience Network")
        # COMPOSITION mạnh — SN sống chết với 2 mạng kia
        self._dmn = dmn
        self._tpn = tpn
        self._switch_log: list[str] = []

    @property
    def label(self) -> str:
        return "SN"

    def process(self, signal: Signal) -> Signal:
        """Đánh giá salience và chuyển mode."""
        if signal >= self.SWITCH_THRESHOLD:
            if signal.source.startswith("sensory_"):
                self._tpn.activation = signal.strength
                self._dmn.activation = max(
                    0.0, self._dmn.activation - 0.3
                )
                self._mode = NetworkMode.EXTERNAL
                self._switch_log.append("→ EXTERNAL (TPN ON)")
            elif signal.source.startswith("internal_"):
                self._dmn.activation = signal.strength
                self._tpn.activation = max(
                    0.0, self._tpn.activation - 0.3
                )
                self._mode = NetworkMode.INTERNAL
                self._switch_log.append("→ INTERNAL (DMN ON)")
        return signal

    @property
    def switch_history(self) -> list[str]:
        # trả bản copy để bảo vệ private state (encapsulation)
        return list(self._switch_log)
