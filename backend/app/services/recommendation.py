from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.flight import FlightOffer
from app.schemas.recommend import FlightQuery, RecommendResponse, RecommendedFlight
from app.services.intent import IntentFeatures, parse_natural_language_intent


async def embed(query: FlightQuery) -> list[float]:
    return [0.0] * 3072


async def search_similar(db: AsyncSession, query: FlightQuery):
    stmt = (
        select(FlightOffer)
        .where(FlightOffer.price_total <= query.budget)
        .limit(100)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


def score_offer(offer: FlightOffer, intent: IntentFeatures) -> float:
    price_score = max(0.0, 1.0 - float(offer.price_total) / 1000.0)
    duration_score = 0.6 if intent.prefers_less_fatigue else 0.3
    stop_penalty = 0.2 if intent.avoid_stops else 0.05
    # raw_payload parsing은 추후 표준화 컬럼(duration_min, stops, depart_hour)로 교체
    heuristic = 0.0
    heuristic += price_score * (0.6 if intent.prefers_low_price else 0.35)
    heuristic += duration_score
    heuristic -= stop_penalty
    if intent.avoids_night:
        heuristic += 0.1
    return heuristic


async def recommend_flights(query: FlightQuery, flights: list[FlightOffer]) -> RecommendResponse:
    intent = parse_natural_language_intent(query.preferences)
    ranked = sorted(flights, key=lambda f: score_offer(f, intent), reverse=True)
    picks = [
        RecommendedFlight(
            offer_id=str(f.id),
            reason="가격/피로도/경유 페널티를 종합한 AI 점수 상위 결과",
            price_total=float(f.price_total),
            currency=f.currency,
        )
        for f in ranked[:5]
    ]
    return RecommendResponse(answer="자연어 취향을 반영한 추천 결과입니다.", flights=picks)


async def recommend_pipeline(query: FlightQuery, db: AsyncSession):
    _ = await embed(query)
    flights = await search_similar(db, query)
    answer = await recommend_flights(query, flights)
    return answer
