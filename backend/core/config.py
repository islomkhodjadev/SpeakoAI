
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    AI_API: str = os.getenv("AI_API")
    VOICE2TEXT: str = os.getenv("VOICE2TEXT")

settings = Settings()
