import os
from pathlib import Path

from dotenv import load_dotenv


# load environment variables from .env
load_dotenv()


class Config:
    """
    Base configuration class
    """
    BASE_DIR = Path(__file__).resolve().parent
    # read from .env file
    SECRET_KEY = os.getenv("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = "sqlite:///network.db"
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_DATABASE
    )
