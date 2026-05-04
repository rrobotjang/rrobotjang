from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.flight import FlightOffer
from app.schemas.recommend import FlightQuery, RecommendResponse, RecommendedFlight


async def embed(query: FlightQuery) -> list[float]:
    return [0.0] * 3072


async def search_similar(db: AsyncSession, q_emb: list[float], query: FlightQuery):
    stmt = (
        select(FlightOffer)
        .where(FlightOffer.price_total <= query.budget)
        .order_by(text("embedding <=> :emb"))
        .params(emb=q_emb)
        .limit(20)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def recommend_flights(query: FlightQuery, flights: list[FlightOffer]) -> RecommendResponse:
    picks = [
        RecommendedFlight(
            offer_id=str(f.id),
            reason="예산/일정/경로 유사도 기준 상위 결과",
            price_total=float(f.price_total),
            currency=f.currency,
        )
        for f in flights[:5]
    ]
    return RecommendResponse(answer="요청 조건과 유사한 항공권 추천 결과입니다.", flights=picks)


async def recommend_pipeline(query: FlightQuery, db: AsyncSession):
    q_emb = await embed(query)
    flights = await search_similar(db, q_emb, query)
    answer = await recommend_flights(query, flights)
    return answer
