from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Zákoník API"
    OPENAI_API_KEY: str
    PROD: bool = True
    origins = [
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://aizakonik.cz",
    ]
    chroma_vectorstore_dir: str = "app/data/chromadb"


settings = Settings()
