import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    """
    Base configuration class
    """
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///network.db'

