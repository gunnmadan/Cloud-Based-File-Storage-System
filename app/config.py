import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://user:password@localhost/cloud_storage'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CREDENTIALS_FILE = 'credentials.json'