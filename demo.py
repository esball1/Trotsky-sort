import time
from core import TrotskyScheduler
from policy import Event
from policy import StandardPriorityPolicy
from profiles import ProfilePreset


def context_fn(e: Event) -> float:
    return 2.0 if e.event_type == "CRITICAL" else 1.0


if __name__ == "__main__":
    profile = ProfilePreset.LATENCY_CRITICAL.value
    policy = StandardPriorityPolicy()

    scheduler = TrotskyScheduler(
        policy=policy,
        block_size=profile.block_size,
        disorder_threshold=profile.disorder_threshold,
    )

    for i in range(20):
        scheduler.push(
            Event(
                event_type="CRITICAL" if i % 5 == 0 else "NORMAL",
                payload=f"job-{i}",
                base_priority=float(i),
                context_fn=context_fn,
                profile=profile,
            )
        )

    for _ in range(5):
        scheduler.revolution_step()
        time.sleep(0.05)

    while True:
        e = scheduler.pop()
        if not e:
            break
        print(
            f"{e.payload} | score={e._current_score:.2f} | "
            f"overtaken={e.times_overtaken} | revs={e.revolutions_survived}"
        )
