from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_chat.db"
    SECRET_KEY: str = "default-insecure-key-change-it"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    # AI Settings
    AI_PROVIDER: str = "ollama" # "ollama" or "openai"
    OPENAI_API_BASE: str = "https://api.groq.com/openai/v1"
    OPENAI_API_KEY: str = "your-api-key"
    OPENAI_MODEL: str = "llama3-8b-8192"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
