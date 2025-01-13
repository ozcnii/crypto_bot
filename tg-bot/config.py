from os import getenv

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Подключение к базе данных SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключение предупреждений о модификациях

class DevelopmentConfig(Config):
    HOST = 'http://backend:5000'
    DEBUG = True
    BOTLINK = getenv('BOT_LINK')
    TOKEN=getenv('TELEGRAM_API_TOKEN')
    WEBAPP_URL = getenv('WEBAPP_URL')

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False