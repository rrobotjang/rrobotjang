from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SimulationMetrics:
    total_offers: int
    budget_fit_count: int
    top1_price: float
    avg_price: float
    success_rate: float


def load_mock_offers(path: str | Path) -> list[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("mock data must be a list")
        return data
    except Exception as exc:
        raise RuntimeError(f"failed to load mock offers: {exc}") from exc


def run_recommendation_simulation(path: str | Path, budget: float) -> SimulationMetrics:
    try:
        offers = load_mock_offers(path)
        filtered = [o for o in offers if float(o["price_total"]) <= budget]
        ranked = sorted(filtered, key=lambda x: (-float(x["embedding_score"]), float(x["price_total"])))

        if not ranked:
            return SimulationMetrics(
                total_offers=len(offers), budget_fit_count=0, top1_price=0.0, avg_price=0.0, success_rate=0.0
            )

        avg_price = sum(float(x["price_total"]) for x in ranked) / len(ranked)
        success_rate = len(ranked) / max(len(offers), 1)

        return SimulationMetrics(
            total_offers=len(offers),
            budget_fit_count=len(ranked),
            top1_price=float(ranked[0]["price_total"]),
            avg_price=avg_price,
            success_rate=success_rate,
        )
    except Exception as exc:
        raise RuntimeError(f"simulation failed: {exc}") from exc
