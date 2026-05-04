from datetime import date
from pydantic import BaseModel, Field


class FlightQuery(BaseModel):
    origin: str = Field(min_length=3, max_length=3)
    destination: str = Field(min_length=3, max_length=3)
    departure_date: date
    return_date: date | None = None
    budget: float
    preferences: list[str] = []


class RecommendedFlight(BaseModel):
    offer_id: str
    reason: str
    price_total: float
    currency: str


class RecommendResponse(BaseModel):
    answer: str
    flights: list[RecommendedFlight]
