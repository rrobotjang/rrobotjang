from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    KAKAO_WEBHOOK_URL: str = ""
    ALERT_ERROR_RATE_THRESHOLD: float = 0.1
    ALERT_P95_MS_THRESHOLD: int = 1200


settings = Settings()
