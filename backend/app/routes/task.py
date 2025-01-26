from flask import Blueprint, jsonify, request
from app.models import Users, Clans, Task
from app import db, responseError, responseSuccess, getToken, auth_required
from telebot import TeleBot
from config import DevelopmentConfig

bp = Blueprint('task', __name__)

#Вернуть все таски
@bp.route('/task', methods=['GET'])
@auth_required
def task():
    #Обработка данных
    return jsonify([x.get_dict() for x in Task.query.all()])

#Обработать таски
@bp.route('/task/<id:int>/completa', methods=['GET'])
@auth_required
def task_completa(id):
    #Обработка данных 4 type
    task: Task = Task.query.filter(Task.id==id).first()
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    
    if task:
        return jsonify(responseError("Такого задания нет"))
    
    #Добыть монеты
    if task.type == "mining":
        if user.balance_features >= task.quest:
            return jsonify(responseSuccess())
        else:
            return jsonify(responseError("Задание не выполнено"))
           
    #Пригласить пользователей 
    elif task.type == "invite":
        if len(user.referals) >= int(task.quest):
            return jsonify(responseSuccess())
        else:
            return jsonify(responseError("Задание не выполнено"))
    
    #Подписаться на канал
    elif task.type == "subscribe":
        bot = TeleBot(DevelopmentConfig.TOKEN)
        try:
            bot.get_chat_member(task.quest.replace("https://t.me/",''), user.chat_id)
            return jsonify(responseSuccess())
        except:
            return jsonify(responseError("Задание не выполнено"))
    
    #Найти клан
    elif task.type == "join":
        if user.clan:
            return jsonify(responseSuccess())
        else:
            return jsonify(responseError("Задание не выполнено"))
    
    else:
        return jsonify(responseError("Неверные данные"))

@bp.after_request
def allow_everyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response