from fastapi import FastAPI
from app.flight_api import router as flight_router
from mangum import Mangum

app = FastAPI(title="Flight API (Serverless)")
app.include_router(flight_router)
handler = Mangum(app)
