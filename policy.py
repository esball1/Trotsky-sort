from abc import ABC, abstractmethod
import time


class PriorityPolicy(ABC):
    """
    Interface of politcy of priority scoring.
    """

    @abstractmethod
    def score(self, event, now: float) -> float:
        pass


class StandardPriorityPolicy(PriorityPolicy):
    """
    Política:
    prioridade_base * contexto + aging
    """

    def score(self, event, now: float) -> float:
        age = now - event.created_at
        context_multiplier = event.context_fn(event)

        priority = (
            event.base_priority * context_multiplier
            + age * event.profile.aging_factor
        )

        # Anti-starvation
        if age > event.profile.starvation_limit_seconds:
            priority += event.profile.emergency_boost

        event._current_score = priority
        return priority
