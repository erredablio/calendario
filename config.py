# config.py
from dotenv import load_dotenv
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///calendar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 3600

