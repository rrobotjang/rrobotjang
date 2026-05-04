from fastapi import FastAPI
from app.monitoring import router as monitoring_router
from mangum import Mangum

app = FastAPI(title="Monitoring API (Serverless)")
app.include_router(monitoring_router)
handler = Mangum(app)
