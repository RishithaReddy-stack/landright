from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AWS
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket_name: str = "landright-knowledge"

    # Bedrock
    bedrock_model_id: str = "meta.llama3-8b-instruct-v1:0"

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    collection_name: str = "landright_docs"

    class Config:
        env_file = ".env"

settings = Settings()
