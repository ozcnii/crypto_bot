from os import getenv

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Подключение к базе данных SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключение предупреждений о модификациях

class DevelopmentConfig(Config):
    HOST = 'http://127.0.0.1:5500'
    DEBUG = True
    BOTLINK = getenv('BOT_LINK')
    TOKEN=getenv('TELEGRAM_API_TOKEN')
    TELEGRAM_BOT_AUTH_TOKEN = getenv('TELEGRAM_BOT_AUTH_TOKEN')#"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZyI6ImJvdCJ9.WW6sya_8HSA0DWdaHC2uqj4HYSynUiEZzsbSBP4VKaI"

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False