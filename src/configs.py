import os
from aws_lambda_powertools import Logger

ENV = os.environ.get("ENV", "dev")
logger = Logger(service=f"{ENV}-your-bot")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")


BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TLG_BASE_URL = os.environ.get("TLG_BASE_URL", "https://api.telegram.org")
TLG_BOT_URL = f"{TLG_BASE_URL}/bot{BOT_TOKEN}"
TLG_SEND_MESSAGE_URL = f"{TLG_BOT_URL}/sendMessage"
TLG_ANSWER_CALLBACK_URL = f"{TLG_BOT_URL}/answerCallbackQuery"
ROW_BUTTONS = os.environ.get("ROW_BUTTONS", "2")

# DATABASE CONFIGURATION
DB_NAME = os.environ.get("DB_NAME", "your_db")
CONNECTION_STR = os.environ.get("CONNECTION_STR", f"mongodb+srv://username:password@your-mongo-cluster.m3cxx.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
