import os

class Config:
    # set these Environment variables should be set in your OS, or .flaskenv for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 