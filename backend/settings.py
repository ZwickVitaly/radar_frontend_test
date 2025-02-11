import os

SECRET_KEY = os.getenv("DB_HOST", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1000

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "radar_test")
DB_USER = os.getenv("DB_USER", "radar_test")
DB_PASSWORD = os.getenv("DB_PASSWORD", "radar_test_123")