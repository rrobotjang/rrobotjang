from fastapi import FastAPI
from app.payment import router as payment_router
from mangum import Mangum

app = FastAPI(title="Payment API (Serverless)")
app.include_router(payment_router)
handler = Mangum(app)
