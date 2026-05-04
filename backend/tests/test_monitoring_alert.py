from app.services.metrics import record_metric, get_health_snapshot


def test_monitoring_snapshot_has_metrics():
    record_metric(100, False)
    record_metric(1800, True)
    snap = get_health_snapshot()
    assert snap["count"] >= 2
    assert snap["p95_ms"] >= 100
    assert 0 <= snap["error_rate"] <= 1
