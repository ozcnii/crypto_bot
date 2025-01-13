from flask import Blueprint, jsonify, request, abort
from app.models import Users
from app import db
import json
from config import DevelopmentConfig
from traceback import print_exc

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET', 'POST', 'DELETE'])
def users():
    response = None
    
    #Получение всех пользователей
    if request.method == "GET":
        response = []
        all_users = Users.query.all()
        for user in all_users:
            response.append(
                user.get_dict()
            )
        return jsonify(response)
    
    #Добавление пользователей
    if request.method == "POST":
        response = None
        
        try:
            data = json.loads(request.data.decode('utf-8'))
            # print("data -> ",data)
            user = Users(**data)
            if not Users.query.filter_by(chat_id=user.chat_id).first() and not Users.query.filter_by(username=user.username).first():
                user.balance_features=user.balance
                db.session.add(user)
                db.session.commit()
                response = {"success":True}
            else:
                response = {"success":False, "error": "Такой пользователь уже сущесвует"}
        except Exception as error:
            response = {"success":False, "error": str(error)}
            print_exc()
            
        return jsonify(response)
            
    #Удаление пользователей
    if request.method == "DELETE":
        response = None
        
        try:
            data = json.loads(request.data.decode('utf-8'))
            # print("data -> ",data)
            user = Users.query.filter_by(chat_id=data["chat_id"]).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                response = {"success":True, "code":200}
            else:
                response = {"success":False, "error": "Такого пользователя не сущесвует"}
        except Exception as error:
            response = {"success":False, "error": str(error)}
            
        return jsonify(response)
    
#Получение списка всех пользователей
@bp.route('/users/<int:chat_id>', methods=['GET', 'PUT']) #GET -> Все пользователи в JSON {[...{}]}
def users_search(chat_id):
    response = None
    
    if request.method == "GET":
        try:
            user = Users.query.filter_by(chat_id=chat_id).first()
            if user:
                response=user.get_dict()
            else:
                response = {"success":False, "error": "Такого пользователя не сущесвует"}
        except Exception as error:
            response = {"success":False, "error": str(error)}
            
        return jsonify(response)

    if request.method == "PUT":
        try:
            data = json.loads(request.data.decode('utf-8'))
            user = Users.query.filter_by(chat_id=chat_id).first()
            if user:
                for param in data.keys():
                    setattr(user, param, data[param])
                db.session.commit()
                response = {"success": True}
            else:
                response = {"success":False, "error": "Такого пользователя не сущесвует"}
        except Exception as error:
            response = {"success":False, "error": str(error)}
            
        return jsonify(response)
@bp.route('/users/<int:chat_id>/getreflink', methods=['GET']) #GET -> Все пользователи в JSON {[...{}]}
def users_getreflink(chat_id):
    response = None
    
    try:
        user: Users = Users.query.filter_by(chat_id=chat_id).first()
        if user:
            response={"success":True}
        else:
            response = {"success":False, "error": "Такого пользователя не сущесвует"}
    except Exception as error:
        response = {"success":False, "error": str(error)}
        
    return jsonify(response)