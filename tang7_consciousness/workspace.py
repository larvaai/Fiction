"""
============================================================
 workspace.py — GLOBAL WORKSPACE (sân khấu ý thức)
 Demo:
   - Singleton (chỉ 1 sân khấu duy nhất - dùng __new__)
   - Context Manager (with workspace as ws: ...)
   - Container protocol (__len__, __iter__, __contains__,
                         __getitem__)
============================================================
"""

from .core import BrainModule, ConsciousnessState, Signal


class GlobalWorkspace:
    """SINGLETON — chỉ một workspace tồn tại trong não."""

    _instance: "GlobalWorkspace | None" = None
    CAPACITY = 4    # Cowan's magic number — ý thức giữ tối đa ~4 items

    # ---- Singleton qua __new__ ----
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._stage: list[Signal] = []
        self._state: ConsciousnessState = ConsciousnessState.AWAKE
        self._broadcast_log: list[str] = []
        self._initialized = True

    # ---- Core ops ----
    def ignite(self, signal: Signal) -> bool:
        """Đưa signal lên 'sân khấu' nếu vượt threshold."""
        if signal < BrainModule.THRESHOLD_CONSCIOUS:
            return False
        # Chỉ giữ tối đa CAPACITY signal — đẩy cũ ra
        if len(self._stage) >= self.CAPACITY:
            self._stage.pop(0)
        self._stage.append(signal)
        return True

    def broadcast(self, modules: list[BrainModule]) -> None:
        """Gửi top signal đến mọi module — lan tỏa toàn cục."""
        if not self._stage:
            return
        top = self._stage[-1]
        for m in modules:
            top << m            # operator overload: signal << module
        self._broadcast_log.append(
            f"broadcast {top!r} -> {len(modules)} modules"
        )

    @property
    def state(self) -> ConsciousnessState:
        return self._state

    @state.setter
    def state(self, value: ConsciousnessState) -> None:
        self._state = value

    # ---- Container protocol (giả làm list) ----
    def __len__(self) -> int:
        return len(self._stage)

    def __iter__(self):
        return iter(self._stage)

    def __contains__(self, signal: Signal) -> bool:
        return signal in self._stage

    def __getitem__(self, idx):
        return self._stage[idx]

    def __bool__(self) -> bool:
        return bool(self._stage)

    # ---- Context manager (with ...) ----
    def __enter__(self):
        # Khi enter: đảm bảo AWAKE để xử lý
        self._previous_state = self._state
        self._state = ConsciousnessState.AWAKE
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Khi exit: trở về state cũ
        self._state = self._previous_state
        return False    # KHÔNG nuốt exception

    def __repr__(self):
        return (
            f"GlobalWorkspace(state={self._state.name}, "
            f"stage_size={len(self._stage)}/{self.CAPACITY})"
        )

    # ---- Cleanup helper for testing ----
    @classmethod
    def reset(cls):
        cls._instance = None
