"""Alert delivery helpers for external messaging channels."""

import httpx
from app.core.config import settings


async def _post_with_retry(url: str, payload: dict, success_codes: set[int], retries: int = 3) -> bool:
    """Send a POST request with retry semantics.

    Args:
        url: Target webhook or API endpoint.
        payload: JSON body sent to the endpoint.
        success_codes: HTTP status codes treated as success.
        retries: Total number of attempts before giving up.

    Returns:
        True if any attempt receives a success status code; otherwise False.
    """
    for _ in range(retries):
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                res = await client.post(url, json=payload)
            if res.status_code in success_codes:
                return True
        except Exception:
            continue
    return False


async def send_telegram_alert(message: str) -> bool:
    """Send an alert message to Telegram with up to 3 retries on failure."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": message}
    return await _post_with_retry(url, payload, {200}, retries=3)


async def send_kakao_alert(message: str) -> bool:
    """Send an alert message to Kakao webhook with up to 3 retries on failure."""
    if not settings.KAKAO_WEBHOOK_URL:
        return False

    payload = {"text": message}
    return await _post_with_retry(settings.KAKAO_WEBHOOK_URL, payload, {200, 201, 204}, retries=3)


async def notify_all(message: str) -> dict:
    """Dispatch the same alert message to Telegram and Kakao channels."""
    telegram_ok = await send_telegram_alert(message)
    kakao_ok = await send_kakao_alert(message)
    return {"telegram": telegram_ok, "kakao": kakao_ok}
