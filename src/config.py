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


AUTH_LIST = os.environ["AUTH_LIST"].split(",")
REWRITE_PROMPT = False


bot = AsyncTeleBot(token=Settings.TG_API_TOKEN, disable_web_page_preview=True)


client = genai.Client(api_key=Settings.GEMINI_API_KEY)
GEMINI_MODEL = "models/gemini-1.5-pro-latest"
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
