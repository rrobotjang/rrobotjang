from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.recommend import FlightQuery, RecommendResponse
from app.services.recommendation import recommend_pipeline

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(query: FlightQuery, db: AsyncSession = Depends(get_db)):
    return await recommend_pipeline(query, db)
