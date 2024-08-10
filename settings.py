import logging
import os

import telebot
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


# Postgres

USER = os.getenv("POSTGRES_USER", "postgres")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE = os.getenv("POSTGRES_DB_NAME", "vocabulary")

engine = create_engine(
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)


# Logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(
    handlers=[
        logging.FileHandler(f"{BASE_DIR}/logs.log"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
    format=(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s - "
        "%(filename)s:%(lineno)s"
    ),
)
logger = logging.getLogger("VocabularyBot")


# Telegram

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
