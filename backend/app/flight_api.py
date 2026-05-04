from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.recommend import FlightQuery, RecommendResponse
from app.services.recommendation import recommend_pipeline

router = APIRouter(prefix="/flight", tags=["flight"])


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(query: FlightQuery, db: AsyncSession = Depends(get_db)):
    try:
        return await recommend_pipeline(query, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="internal recommendation error") from exc
