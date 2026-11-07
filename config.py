"""
Configuration settings for Cricket Analytics Web Application.
Loads environment variables safely with robust defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the project root
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "cricket_analytics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "oslab")

APP_TITLE = "Cricket Analytics Hub"
APP_SUBTITLE = "IPL 2025 Performance, Statistics & Match Analysis"

