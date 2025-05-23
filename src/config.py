import os

from google import genai
from google.genai import types
from telebot.async_telebot import AsyncTeleBot

if os.environ.get("ENV") != "PROD":
    from dotenv import load_dotenv

    load_dotenv()


class Settings:
    RAGIE_API_KEY = os.environ["RAGIE_API_KEY"]
    GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
    TG_API_TOKEN = os.environ["TG_API_TOKEN"]
    DATABASE_URL = os.environ["DATABASE_URL"]
    SENTRY_DSN = os.environ.get("SENTRY_DSN")
    REWRITE_PROMPT = False
    CHAT_IDS = os.environ["CHAT_IDS"].split(",")


settings = Settings()


bot = AsyncTeleBot(token=settings.TG_API_TOKEN, disable_web_page_preview=True)


client = genai.Client(api_key=settings.GEMINI_API_KEY)
# gemini-1.5-pro or gemini-2.5-flash-preview-05-20
GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"
SAFETY_SETTINGS = [
    types.SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="BLOCK_NONE",
    ),
    types.SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="BLOCK_NONE",
    ),
    types.SafetySetting(
        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold="BLOCK_NONE",
    ),
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_NONE",
    ),
]
