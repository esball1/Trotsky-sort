import time
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass
class Event:
    event_type: str
    payload: Any
    base_priority: float
    context_fn: Callable[['Event'], float]
    created_at: float = field(default_factory=time.time)

    def priority(self, now: float, aging_factor: float) -> float:
        age = now - self.created_at
        context_multiplier = self.context_fn(self)
        return self.base_priority * context_multiplier + age * aging_factor


class TrotskyQueue:
    def __init__(
        self,
        block_size: int = 16,
        disorder_threshold: float = 0.3,
        aging_factor: float = 0.01
    ):
        self._events: List[Event] = []
        self.block_size = block_size
        self.disorder_threshold = disorder_threshold
        self.aging_factor = aging_factor

    # Public API 

    def push(self, event: Event) -> None:
        self._events.append(event)

    def pop(self) -> Optional[Event]:
        if not self._events:
            return None

        now = time.time()
        
        max_index = 0
        max_priority = self._events[0].priority(now, self.aging_factor)
        
        for i in range(1, len(self._events)):
            current_priority = self._events[i].priority(now, self.aging_factor)
            if current_priority > max_priority:
                max_priority = current_priority
                max_index = i
        
        return self._events.pop(max_index)

    def revolution_step(self) -> None:
        now = time.time()
        n = len(self._events)

        for start in range(0, n, self.block_size):
            end = min(start + self.block_size, n)
            if end - start < 2:
                continue

            if self._local_disorder(start, end, now) > self.disorder_threshold:
                self._local_reorder(start, end, now)

    def snapshot(self):
        now = time.time()
        return [
            {
                "type": e.event_type,
                "priority": round(e.priority(now, self.aging_factor), 3),
                "age": round(now - e.created_at, 2),
            }
            for e in self._events
        ]

    # ---- Internal mechanics... Somone really reads the comments? ----

    def _local_disorder(self, start: int, end: int, now: float) -> float:
        inversions = 0
        total = end - start - 1

        for i in range(start, end - 1):
            if self._priority(i, now) < self._priority(i + 1, now):
                inversions += 1

        if total == 0:
            return 0.0
            
        return inversions / total

    def _local_reorder(self, start: int, end: int, now: float) -> None:
        for i in range(start + 1, end):
            current = self._events[i]
            current_priority = current.priority(now, self.aging_factor)

            j = i - 1
            while (
                j >= start
                and self._events[j].priority(now, self.aging_factor) < current_priority
            ):
                self._events[j + 1] = self._events[j]
                j -= 1

            self._events[j + 1] = current

    def _priority(self, index: int, now: float) -> float:
        return self._events[index].priority(now, self.aging_factor)
