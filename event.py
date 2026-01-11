import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Event:
    """
   basis of the scheduling unit.

    the event don't know about the scheduler,
    but it loads the profile and context function to be used by the policy.
    """

    event_type: str
    payload: Any
    base_priority: float
    context_fn: Callable[['Event'], float]
    profile: Any

    created_at: float = field(default_factory=time.time)
    revolutions_survived: int = 0
    times_overtaken: int = 0
    _current_score: float = 0.0
