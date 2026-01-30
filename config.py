import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# GCP Settings
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1") # Default to us-central1
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

DB_NAME = "news_history.db"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
FETCH_INTERVAL_MINUTES = 30
