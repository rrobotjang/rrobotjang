from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["frontend"])


@router.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html><body><h1>Flight AI</h1><p>Use /docs for API.</p></body></html>
    """
