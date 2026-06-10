import logging
import os

import telebot
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import create_engine

load_dotenv()


ENVIRONMENT = os.getenv("ENVIRONMENT")


# Postgres

USER = os.getenv("POSTGRES_USER", "postgres")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE = os.getenv("POSTGRES_DB_NAME", "vocabulary")

engine = create_engine(
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
)


# Logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(
    handlers=[
        logging.FileHandler(f"{BASE_DIR}/logs.log"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
    format=("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)s"),
)
logger = logging.getLogger("VocabularyBot")


# Telegram

ADMIN_USER_TELEGRAM_ID = os.getenv("ADMIN_USER_TELEGRAM_ID")
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT"))
bot = telebot.TeleBot(TOKEN)


# OpenAI

GPT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
