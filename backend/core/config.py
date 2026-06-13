from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    postgres_url: str = ""
    collection_name: str = "landright_docs"

    class Config:
        env_file = ".env"

settings = Settings()