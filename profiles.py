from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class SchedulerProfile:
    block_size: int = 16
    disorder_threshold: float = 0.3
    aging_factor: float = 0.01

    starvation_limit_seconds: float = 60.0
    emergency_boost: float = 1000.0


class ProfilePreset(Enum):
    LATENCY_CRITICAL = SchedulerProfile(
        block_size=4,
        disorder_threshold=0.1,
        aging_factor=0.05,
    )

    THROUGHPUT_CRITICAL = SchedulerProfile(
        block_size=64,
        disorder_threshold=0.5,
        aging_factor=0.001,
    )

    FAIRNESS_CRITICAL = SchedulerProfile(
        block_size=16,
        disorder_threshold=0.3,
        starvation_limit_seconds=10.0,
        emergency_boost=5000.0,
    )
