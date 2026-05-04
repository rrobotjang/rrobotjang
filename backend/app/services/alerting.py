import httpx
from app.core.config import settings


async def send_telegram_alert(message: str) -> bool:
    try:
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            return False
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": message}
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.post(url, json=payload)
        return res.status_code == 200
    except Exception:
        return False


async def send_kakao_alert(message: str) -> bool:
    try:
        if not settings.KAKAO_WEBHOOK_URL:
            return False
        payload = {"text": message}
        async with httpx.AsyncClient(timeout=5) as client:
            res = await client.post(settings.KAKAO_WEBHOOK_URL, json=payload)
        return res.status_code in (200, 201, 204)
    except Exception:
        return False


async def notify_all(message: str) -> dict:
    telegram_ok = await send_telegram_alert(message)
    kakao_ok = await send_kakao_alert(message)
    return {"telegram": telegram_ok, "kakao": kakao_ok}
