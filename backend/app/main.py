from fastapi import FastAPI
from app.api.rag import router as rag_router

app = FastAPI(title="Flight AI Platform")
app.include_router(rag_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
