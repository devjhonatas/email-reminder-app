import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-segura'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'chave-jwt-segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lembretes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = 'SUA_CHAVE_API_SENDGRID'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # URL do Redis como broker
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'