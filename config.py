import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set")