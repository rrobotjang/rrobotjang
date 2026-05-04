from fastapi.testclient import TestClient
from app.main import app
import app.flight_api as flight_api

client = TestClient(app)


def test_flight_api_exception_to_500(monkeypatch):
    async def boom(*args, **kwargs):
        raise RuntimeError("db down")

    monkeypatch.setattr(flight_api, "recommend_pipeline", boom)
    res = client.post("/flight/recommend", json={
        "origin": "ICN", "destination": "NRT", "departure_date": "2026-08-01", "budget": 400
    })
    assert res.status_code == 500
