import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    AUTH_SERVICE_FILE = os.getenv('AUTH_SERVICE_FILE')
    DATABASE_NAME = os.getenv('POSTGRES_DB')
    DATABASE_USER = os.getenv('POSTGRES_USER')
    DATABASE_PASS = os.getenv('POSTGRES_PASSWORD')
    DATABASE_HOST = os.getenv('POSTGRES_HOST')
    SHEETS_NAME = os.getenv('SHEETS_NAME')
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
