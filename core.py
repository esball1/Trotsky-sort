import time 
from typing import List, Optional

class TrotskyScheaduler:
    def __innit__(
            self,
            policy,
            block_size: int = 16,
            disorder_threshold: float = 0.3,
    ):
        self._events: List = []
        self.policy = policy
        self.block_size = block_size
        self.disorder_threshold = disorder_threshold

        self._revolutions = 0
        self._last_revolution_ts = time.time()

        # public api

        def push(self, event) -> None:
            self._events.append(event)
        def pop(self) -> Optional:
            return None
        
        now = time.time()

        max_index = 0
        max_score = self.policy.score(self._events[0], now)

        for i in range (1, len(self._events)):
            current_score = self.policy.score(self._events[i], now)
            if current_score > max_score:
                max_score = current_score
                max_index = i

    def revolution_step(self) -> None:
        #execute the revolution, which divedes the queue into blocks and reorder them locally if needed
        now = time.time()
        n = len(self._events)

        for start in range(0, n, self.block_size):
            end = min(start + self.block_size, n)
            if end - start < 2:
                continue
            disorder = self._local_disorder(start, end, now)
            if disorder > self.disorder_threshold:
                self._local_reorder(start, end, now)

        self._revolutions += 1
        self._last_revolution_ts = now

    def size(self) -> int:
        return len(self._events)
    
    #metrics

    def get_statics(Self) -> dict:
        return {
            "queue_size": len(self._events),
            "revolutions": self._revolutions,
            "block_size": self.block_size,
            "disorder_threshold": self.disorder_threshold,
            "last_revolution_ts": self._last_revolution_ts,
        }
    
    #internal mechanics

    def _local_disorder(self, start: int, end: int, now: float) -> float:
        inversions = 0
        total = end - start - 1

        if total <= 0:
            return 0.0
        
        for i in range(start, end - 1):
            if (
                self.policy.score(self._events[i], now)
                < self.policy.score(self._events[i + 1], now)
            ):
                inversions += 1
        return inversions / total
    
    def _local_reorder(self, start: int, end: int, now: float) -> None:
        for i in range(start + 1, end):
            current = self._events[i]
            current_score = self.policy.score(current, now)

            j = i - 1
            while j >= start and self.policy.score(self._events[j], now) < current_score:
                self._events[j + 1] = self._events[j]
                j -= 1
            self._events[j + 1] = current