"""
============================================================
 brain.py — BRAIN: tích hợp toàn bộ Tầng 7
 Demo:
   - COMPOSITION (Brain HAS-A networks, cingulate, workspace)
   - AGGREGATION (memory pool — dùng chung cho nhiều module)
   - DELEGATION (Brain ủy thác việc cho các bộ phận con)
   - DataClass: Experience
============================================================
"""

from dataclasses import dataclass, field
from typing import Iterator

from .cingulate import (
    AnteriorCingulate,
    MidCingulate,
    PosteriorCingulate,
)
from .core import (
    BrainModule,
    ConsciousnessState,
    Memory,
    Signal,
    TimeDirection,
)
from .networks import (
    DefaultModeNetwork,
    SalienceNetwork,
    TaskPositiveNetwork,
)
from .theories import (
    GWT,
    HOT,
    IIT,
    ConsciousnessAssessor,
    PredictiveProcessing,
)
from .workspace import GlobalWorkspace


# ------------------------------------------------------------
# DataClass: Experience — gói trải nghiệm có ý thức
# ------------------------------------------------------------
@dataclass
class Experience:
    """Một 'moment' ý thức = signal + bộ điểm theory + memories."""
    signal_repr: str
    theory_scores: dict = field(default_factory=dict)
    activated_modules: list = field(default_factory=list)
    is_conscious: bool = False


# ------------------------------------------------------------
# BRAIN — COMPOSITION HUB
# ------------------------------------------------------------
class Brain:
    """Sinh vật Tầng 7. Composition: Brain HAS-A everything."""

    def __init__(self, name: str = "Ellumm-7"):
        self.name = name

        # --- Composition: tạo các network nội bộ ---
        self.dmn = DefaultModeNetwork()
        self.tpn = TaskPositiveNetwork()
        self.sn = SalienceNetwork(self.dmn, self.tpn)

        # --- Cingulate (3 vùng) ---
        self.acc = AnteriorCingulate()
        self.mcc = MidCingulate()
        self.pcc = PosteriorCingulate()

        # --- Singleton workspace ---
        self.workspace = GlobalWorkspace()

        # --- Aggregation: memory pool dùng chung ---
        self._memory_pool: list[Memory] = []

        # --- Higher-Order monitor cần module — dùng PCC ---
        self._assessor = (
            ConsciousnessAssessor(GWT(), IIT(), PredictiveProcessing())
            .add(HOT(monitor_module=self.pcc))   # method chaining
        )

        # --- Connect modules theo wiring ---
        self.sn.connect(self.dmn).connect(self.tpn)
        self.acc.connect(self.pcc).connect(self.mcc)

    # ---- Encapsulation: expose dạng read-only ----
    @property
    def all_modules(self) -> list[BrainModule]:
        return [self.dmn, self.tpn, self.sn,
                self.acc, self.mcc, self.pcc]

    @property
    def memory_count(self) -> int:
        return len(self._memory_pool)

    # ---- Operations ----
    def perceive(self, signal: Signal) -> Experience:
        """Vòng đời 1 stimulus: SN -> route -> ignition -> broadcast."""
        # 1) SN đánh giá salience -> chuyển mode
        self.sn(signal)
        # 2) PCC gate consciousness
        self.pcc.gate_consciousness(signal.strength)
        # 3) ignite vào workspace nếu đủ mạnh
        ignited = self.workspace.ignite(signal)
        # 4) broadcast nếu ignite
        if ignited:
            self.workspace.broadcast(self.all_modules)
        # 5) chấm điểm bằng 4 theory
        scores = self._assessor.assess_all(signal, self.all_modules)
        # 6) tổng kết
        active = [m.name for m in self.all_modules if m.is_conscious]
        return Experience(
            signal_repr=repr(signal),
            theory_scores=scores,
            activated_modules=active,
            is_conscious=ignited,
        )

    def remember(self, mem: Memory) -> "Brain":
        """Aggregation — memory tồn tại độc lập, brain chỉ giữ reference."""
        self._memory_pool.append(mem)
        return self

    def mental_time_travel(
        self, direction: TimeDirection, cue: str = ""
    ) -> str:
        """Delegation — DMN làm phần lớn việc."""
        if not self._memory_pool:
            return "(không có ký ức để du hành)"
        if direction == TimeDirection.PAST:
            mem = max(self._memory_pool)   # max theo emotional_tag
            return f"[PAST] sống lại: {mem.content!r} (cảm xúc {mem.emotional_tag:+.2f})"
        if direction == TimeDirection.FUTURE:
            chain = self.dmn.mind_wander(cue or "ngày mai", steps=3)
            return f"[FUTURE] tưởng tượng: {' → '.join(chain)}"
        # COUNTERFACTUAL
        mem = self._memory_pool[-1]
        return f"[WHAT-IF] giả sử {mem.content!r} đã KHÁC..."

    def metacognize(self) -> dict:
        """Higher-order: 'tôi đang nghĩ gì?' — báo cáo trạng thái."""
        return {
            "name": self.name,
            "state": self.workspace.state.name,
            "workspace_size": len(self.workspace),
            "memory_count": self.memory_count,
            "modules_conscious": [
                m.name for m in self.all_modules if m.is_conscious
            ],
            "dmn_mode": self.sn.mode.name,
        }

    # ---- Context manager: tạm vào trạng thái khác ----
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    # ---- Iterator: stream of consciousness ----
    def __iter__(self) -> Iterator[Signal]:
        """Lặp qua workspace — duck typing như list."""
        return iter(self.workspace)

    def __len__(self) -> int:
        return len(self.all_modules)

    def __repr__(self) -> str:
        return (
            f"Brain(name={self.name!r}, "
            f"modules={len(self)}, memories={self.memory_count}, "
            f"state={self.workspace.state.name})"
        )

    def __str__(self) -> str:
        lines = [f"=== {self.name} ===",
                 f"State: {self.workspace.state.name}",
                 f"Workspace: {len(self.workspace)}/{GlobalWorkspace.CAPACITY}",
                 "Modules:"]
        for m in sorted(self.all_modules, reverse=True):  # __lt__
            lines.append(f"  {m}")    # dùng __str__ của module
        return "\n".join(lines)
