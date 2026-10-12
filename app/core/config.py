import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "NexusRAG API"
    LLAMA3_API_URL: str = os.getenv("LLAMA3_API_URL")
    LLAMA3_API_KEY: str = os.getenv("LLAMA3_API_KEY")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    DATA_DIR: str = "./data"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
os.makedirs(settings.DATA_DIR, exist_ok=True)