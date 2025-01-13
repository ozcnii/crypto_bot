from flask import Blueprint, jsonify, request, abort
from app.models import Users, Clans
from app import db
import json
from config import DevelopmentConfig
import datetime as dt

bp = Blueprint('clans', __name__)

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.data_dict = entries
    
        
def responseSuccess(**data):
    d = {}; d.update(**data, success=True)
    return d

def responseError(error):
    d = {}; d.update(success=False, error=error)
    return d

#Работа с кланами
@bp.route('/clans', methods=['GET', 'POST', 'PUT', 'DELETE'])
def clans(): 
    #Получение списка всех кланов
    if request.method == "GET":
        clans: Clans = Clans.query.all()
        return jsonify(clans)
    
    #Создание клана
    if request.method == "POST":
        data = Struct(
            **json.loads(request.data.decode())
        )
        user: Users = Users.query.filter_by(chat_id=data.admin).first()
        
        if user:
            if not user.clan:
                if not Clans.query.filter_by(peer=data.peer).first():
                    db.session.add(
                        Clans(
                            peer=data.peer,
                            admin=data.admin,
                            users=data.users,
                            league=data.league,
                            name=data.name,                            
                        )
                    )
                    
                    user.clan = data.peer
                    
                    db.session.commit()
                    return jsonify(responseSuccess())
                else:
                  return jsonify(responseError("Такой клан уже существует"))  
            else:
                return jsonify(responseError("Клан пользователя уже создан"))
        else:
            return jsonify(responseError("Пользователя не существует"))
        
    #Обновление данных о клане
    if request.method == "PUT":
        data = Struct(
            **json.loads(request.data.decode())
        )
        
        clan: Clans = Clans.query.filter_by(peer=data.peer).first()
        if not clan: clan: Clans = Clans.query.filter_by(id=data.id).first()
        
        if clan:
            for i in data.data_dict:
                setattr(clan, i, data.data_dict[i])
                
            db.session.commit()
            return jsonify(responseSuccess())
        else:
            return jsonify(responseError("Такого клана не существует"))
        
    #Удаление клана
    if request.method == "DELETE":
        data = Struct(
            **json.loads(request.data.decode())
        )
        
        clan: Clans = Clans.query.filter_by(peer=data.peer).first()
        if not clan: clan: Clans = Clans.query.filter_by(id=data.id).first()
        user: Users = Users.query.filter_by(chat_id=data.admin).first()
        
        if clan:
            if user:
                for us in clan.users:
                   cl_user = Users.query.filter_by(chat_id=us).first()
                   if cl_user is not None:
                       cl_user.clan = None
                       
                user.clan=None
                db.session.delete(clan)
                db.session.commit()
                return jsonify(responseSuccess())
            else:
                return jsonify(responseError("Такого пользоватля не существует"))
        else:
            return jsonify(responseError("Такого клана не существует"))
        
#Добавление участника в клан
@bp.route('/clans/addmember/<int:peer>/<int:chat_id>', methods=['GET'])
def clansAddMember(peer, chat_id):
    clan: Clans = Clans.query.filter_by(peer=peer).first()
    if not clan: clan: Clans = Clans.query.filter_by(id=data.id).first()
    user: Users = Users.query.filter_by(chat_id=chat_id).first()
    
    if user:
        if not user.clan:
            if clan:
                if chat_id not in clan.users:
                    nowUsersList = clan.users.copy()
                    nowUsersList.append(chat_id)
                    clan.users = nowUsersList
                    user.clan=clan.peer
                    db.session.commit()
                    return jsonify(responseSuccess())
                else:
                    return jsonify(responseError("Пользователь уже добавлен в этот канал"))
            else:
                return jsonify(responseError("Такого клана не существует"))
        else:
            return jsonify(responseError("Пользователь уже в клане")) 
    else:
        return jsonify(responseError("Такого пользователя не существует"))
    
#Удаление участника из клана
@bp.route('/clans/delmember/<int:peer>/<int:chat_id>', methods=['GET'])
def clansDelMember(peer, chat_id):
    clan: Clans = Clans.query.filter_by(peer=peer).first()
    if not clan: clan: Clans = Clans.query.filter_by(id=data.id).first()
    user: Users = Users.query.filter_by(chat_id=chat_id).first()
    
    if user:
        if user.clan is not None:
            if clan:
                if chat_id in clan.users:
                    nowUsersList = clan.users.copy()
                    nowUsersList.remove(chat_id)
                    user.clan=None
                    clan.users = nowUsersList
                    db.session.commit()
                    return jsonify(responseSuccess())
                else:
                    return jsonify(responseError("Пользователя нет в этом клане"))      
            else:
                return jsonify(responseError("Такого клана не существует")) 
        else:
            return jsonify(responseError("Пользователь не состоит в клане"))    
    else:
        return jsonify(responseError("Такого пользователя не существует"))

#Получение конкретного клана
@bp.route('/clans/get/<int:peer>', methods=['GET'])
def clansGet(peer):
    clan: Clans = Clans.query.filter_by(peer=peer).first()
    if not clan: clan: Clans = Clans.query.filter_by(id=data.id).first()
    
    if clan:
        return jsonify(clan.get_dict())
    else:
        responseError("Такого клана не существует")