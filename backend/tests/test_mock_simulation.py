from app.simulation.mock_simulation import run_recommendation_simulation


def test_mock_simulation_metrics():
    metrics = run_recommendation_simulation("mock_data/flight_offers.json", budget=300)
    assert metrics.total_offers == 5
    assert metrics.budget_fit_count == 3
    assert metrics.top1_price == 220.0
    assert round(metrics.avg_price, 2) == 226.67
    assert round(metrics.success_rate, 2) == 0.60
