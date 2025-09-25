import os

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_NAME = os.environ["DB_NAME"]
SECRET_KEY = os.environ["SECRET_KEY"]
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
