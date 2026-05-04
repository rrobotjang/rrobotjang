from fastapi import APIRouter
from app.core.config import settings
from app.services.alerting import notify_all
from app.services.metrics import record_metric, get_health_snapshot

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/dashboard")
async def dashboard():
    return get_health_snapshot()


@router.post("/simulate-request")
async def simulate_request(duration_ms: float = 100, is_error: bool = False):
    record_metric(duration_ms, is_error)
    return {"ok": True}


@router.post("/check-alert")
async def check_alert():
    snap = get_health_snapshot()
    breach = snap["error_rate"] >= settings.ALERT_ERROR_RATE_THRESHOLD or snap["p95_ms"] >= settings.ALERT_P95_MS_THRESHOLD
    if breach:
        result = await notify_all(f"[ALERT] error_rate={snap['error_rate']} p95={snap['p95_ms']}ms")
        return {"breach": True, "snapshot": snap, "notify": result}
    return {"breach": False, "snapshot": snap}
