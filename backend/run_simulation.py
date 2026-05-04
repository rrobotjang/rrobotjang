from app.simulation.mock_simulation import run_recommendation_simulation

if __name__ == "__main__":
    m = run_recommendation_simulation("mock_data/flight_offers.json", budget=300)
    print({
        "total_offers": m.total_offers,
        "budget_fit_count": m.budget_fit_count,
        "top1_price": m.top1_price,
        "avg_price": round(m.avg_price, 2),
        "success_rate": round(m.success_rate, 2),
    })
