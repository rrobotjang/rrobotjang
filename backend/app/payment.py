"""Simple payment APIs for checkout and payment confirmation."""

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/payment", tags=["payment"])

SUPPORTED_PAYMENT_METHODS = {"card", "bank_transfer", "wallet", "kakao_pay", "naver_pay"}


class PaymentRequest(BaseModel):
    """Checkout request payload for a selected flight offer."""

    offer_id: str
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    method: str


class ConfirmPaymentRequest(BaseModel):
    """Confirmation payload for a previously authorized transaction."""

    transaction_id: str = Field(min_length=1)
    approved: bool = True


@router.post("/checkout")
async def checkout(payload: PaymentRequest):
    """Authorize a simple mock payment and return transaction metadata."""
    try:
        if payload.method not in SUPPORTED_PAYMENT_METHODS:
            raise ValueError("unsupported payment method")

        transaction_id = f"txn_{uuid4().hex[:14]}"
        return {
            "status": "authorized",
            "transaction_id": transaction_id,
            "offer_id": payload.offer_id,
            "amount": round(payload.amount, 2),
            "currency": payload.currency.upper(),
            "method": payload.method,
            "authorized_at": datetime.utcnow().isoformat() + "Z",
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="payment processing error") from exc


@router.post("/confirm")
async def confirm_payment(payload: ConfirmPaymentRequest):
    """Confirm or cancel an authorized mock payment transaction."""
    status = "captured" if payload.approved else "cancelled"
    return {
        "status": status,
        "transaction_id": payload.transaction_id,
        "confirmed_at": datetime.utcnow().isoformat() + "Z",
    }
