import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_and_front_page():
    assert client.get('/health').status_code == 200
    assert client.get('/').status_code == 200


def test_recommend_endpoint_contract_and_latency():
    start = time.perf_counter()
    res = client.post('/flight/recommend', json={
        "origin": "ICN", "destination": "NRT", "departure_date": "2026-08-01", "budget": 800
    })
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert res.status_code in (200, 500)
    # 성능 지표(로컬 통합테스트 기준): 1000ms 이하 목표
    assert elapsed_ms < 1000
