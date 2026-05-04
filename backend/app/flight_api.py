"""Flight recommendation and price alert APIs."""

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.recommend import FlightQuery, RecommendResponse
from app.services.alerting import notify_all
from app.services.recommendation import recommend_pipeline

router = APIRouter(prefix="/flight", tags=["flight"])


class FlightAlertRequest(BaseModel):
    """Request payload to register a fare alert for a flight offer."""

    offer_id: str = Field(min_length=1)
    target_price: float = Field(gt=0)
    current_price: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    message: str = ""


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(query: FlightQuery, db: AsyncSession = Depends(get_db)):
    """Return recommendation results for the incoming query."""
    try:
        return await recommend_pipeline(query, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="internal recommendation error") from exc


@router.post("/alerts")
async def create_price_alert(payload: FlightAlertRequest):
    """Create a fare alert and send immediate notification if target is met."""
    alert_id = f"alert_{uuid4().hex[:12]}"
    should_notify = payload.current_price <= payload.target_price

    alert_state = {
        "alert_id": alert_id,
        "offer_id": payload.offer_id,
        "target_price": payload.target_price,
        "current_price": payload.current_price,
        "currency": payload.currency.upper(),
        "should_notify": should_notify,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }

    if should_notify:
        base_message = (
            f"[항공권 알림] {payload.offer_id} 가격이 목표가 이하입니다: "
            f"{payload.current_price:.2f} {payload.currency.upper()} <= {payload.target_price:.2f} {payload.currency.upper()}"
        )
        message = f"{base_message}\n{payload.message}" if payload.message else base_message
        delivery = await notify_all(message)
        alert_state["notification"] = delivery
    else:
        alert_state["notification"] = {"telegram": False, "kakao": False}

    return alert_state
