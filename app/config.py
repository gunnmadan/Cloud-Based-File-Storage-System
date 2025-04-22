import os
from dotenv import load_dotenv

load_dotenv()

class Config:
<<<<<<< HEAD
    SECRET_KEY = os.environ.get('SECRET_KEY') or '880ed05db0ef83a6b22e0db24622160b'
=======
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
>>>>>>> miracle/main
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://user:password@localhost/cloud_storage'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CREDENTIALS_FILE = 'credentials.json'