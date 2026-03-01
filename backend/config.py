from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./etnografica_potosi.db"
    gemini_api_key: str = ""          # Gratis en: https://aistudio.google.com/apikey
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
