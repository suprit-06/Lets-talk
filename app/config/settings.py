from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_chat.db"
    SECRET_KEY: str = "default-insecure-key-change-it"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    # Groq API Settings
    GROQ_API_KEY: str = "your-groq-api-key"
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
