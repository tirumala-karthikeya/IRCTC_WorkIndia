import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', '1234')  # Set a secret key
    # Use 'DATABASE_URL' as the environment variable key for the database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://railway_user:irctc123@localhost/railway_db')
