import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path="/home/yourusername/NotesManager/.env")

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_NAME = os.environ.get("DB_NAME")

SECRET_KEY = os.environ.get("SECRET_KEY")

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
