"""Baseline price prediction training entrypoint."""
from dataclasses import dataclass


@dataclass
class PriceFeatures:
    days_to_departure: int
    route_popularity: float
    seasonality_idx: float
    carrier_score: float


def predict(features: PriceFeatures) -> float:
    # placeholder rule-based baseline. replace with XGBoost/LGBM.
    return 80 + features.days_to_departure * 1.2 + features.route_popularity * 20
