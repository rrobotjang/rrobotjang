from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/payment", tags=["payment"])


class PaymentRequest(BaseModel):
    offer_id: str
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    method: str


@router.post("/checkout")
async def checkout(payload: PaymentRequest):
    try:
        # TODO: integrate Stripe/Toss gateway and idempotency key
        if payload.method not in {"card", "bank_transfer", "wallet"}:
            raise ValueError("unsupported payment method")
        return {"status": "authorized", "offer_id": payload.offer_id}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="payment processing error") from exc
