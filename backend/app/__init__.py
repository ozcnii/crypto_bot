from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
import jwt
from config import DevelopmentConfig
from functools import wraps

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Проверка токена
        if "Authorization" not in request.headers:
            return jsonify({'error': "Отказано в доступе"}), 503

        # Проверка доступа
        if not checkAuth(request, db.session.query(Users).all()):
            return jsonify({'error': "Не авторизован"}), 401

        # Если все проверки пройдены, вызываем исходную функцию
        return func(*args, **kwargs)

    return wrapper

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.data_dict = entries

def getTokenUser(id, username):
    playload = {
        "id": id,
        "username":username
    }
    
    #Подпись токена
    return jwt.encode(playload, app.config['SECRET_KEY'], algorithm='HS256')

def checkAuth(request, all_users):
    token = request.headers['Authorization'].replace('Bearer ', '')
    
    #Авторизация для телеграм бота
    if DevelopmentConfig.TELEGRAM_BOT_AUTH_TOKEN == token:
        return True
    
    for user in all_users:
        if user.token == token:
            return True
    return False

def getToken(request):
    return request.headers['Authorization'].replace('Bearer ', '')

def responseSuccess(**data):
    d = {}; d.update(**data, success=True)
    return d

def responseError(error):
    d = {}; d.update(success=False, error=error)
    return d

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config.from_object(Config)

# Создаем объект SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Users, Stories, Orders, Boosters, Clans
from app.routes.user import bp as userRoute
from app.routes.stories import bp as storiesRoute
from app.routes.orders import bp as ordersRoute
from app.routes.boosters import bp as boostersRoute
from app.routes.clans import bp as clansRoute
from app.routes.access import bp as accessRoute
from app.routes.apiswagger import SWAGGERUI_BLUEPRINT, SWAGGER_URL

#routes
app.register_blueprint(userRoute)
app.register_blueprint(storiesRoute)
app.register_blueprint(ordersRoute)
app.register_blueprint(boostersRoute)
app.register_blueprint(clansRoute)
app.register_blueprint(accessRoute)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
