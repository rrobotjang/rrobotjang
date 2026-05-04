from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_payment_invalid_method_returns_400():
    res = client.post("/payment/checkout", json={
        "offer_id": "x1", "amount": 100, "currency": "USD", "method": "crypto"
    })
    assert res.status_code == 400


def test_payment_success():
    res = client.post("/payment/checkout", json={
        "offer_id": "x1", "amount": 100, "currency": "USD", "method": "card"
    })
    assert res.status_code == 200
    assert res.json()["status"] == "authorized"
