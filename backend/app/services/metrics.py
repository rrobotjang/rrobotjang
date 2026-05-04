from collections import deque
from statistics import quantiles

REQUEST_TIMES = deque(maxlen=500)
ERROR_FLAGS = deque(maxlen=500)


def record_metric(duration_ms: float, is_error: bool) -> None:
    REQUEST_TIMES.append(duration_ms)
    ERROR_FLAGS.append(1 if is_error else 0)


def get_health_snapshot() -> dict:
    if not REQUEST_TIMES:
        return {"count": 0, "p95_ms": 0.0, "error_rate": 0.0}
    p95 = quantiles(REQUEST_TIMES, n=100)[94] if len(REQUEST_TIMES) >= 20 else max(REQUEST_TIMES)
    error_rate = sum(ERROR_FLAGS) / len(ERROR_FLAGS)
    return {"count": len(REQUEST_TIMES), "p95_ms": round(p95, 2), "error_rate": round(error_rate, 4)}
