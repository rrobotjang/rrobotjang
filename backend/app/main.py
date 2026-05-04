from fastapi import FastAPI
from app.frontend import router as frontend_router
from app.flight_api import router as flight_router
from app.payment import router as payment_router

app = FastAPI(title="Flight AI Platform")
app.include_router(frontend_router)
app.include_router(flight_router)
app.include_router(payment_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
