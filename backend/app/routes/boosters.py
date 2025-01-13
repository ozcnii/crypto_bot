from flask import Blueprint, jsonify, request, abort
from app.models import Boosters, Users, Xboosters
from app import db
import json
from config import DevelopmentConfig
import datetime as dt

bp = Blueprint('boosters', __name__)

#Проверить наличие бустеров
@bp.route('/boosters', methods=['GET'])
def boosters(): 
    if Boosters.query.all() == []:
        db.session.add(Boosters(
            types = [
                "range","leverage","trades"
            ],
            prices = [
                [0,150,300,600,2000,5000,15000,35000,80000,200000],
                [0,150,300,600,2000,5000,15000,35000,80000,250000],
                [0,150,400,1000,3000,8000,20000,50000,200000,1000000],
            ],
            profits = [
                [10,15,25,35,50,65,75,85,95,100],
                [1,3,5,7,10,15,25,50,100,125],
                [1,4,5,6,7,8,9,10,12,-1],
            ]
        ))
        
        db.session.commit()
        return jsonify({'success': False, "error":"Бустеры не инициализированы"})
    else:
        return jsonify({'success': True})
    
#Вернуть все бустеры
@bp.route('/boosters/getall', methods=['GET'])
def boosters_get_all(): 
    boosters: Boosters = Boosters.query.all()
    
    if boosters == []:
        return jsonify({'success': False, "error":"Бустеры не инициализированы"})
    else:
        return jsonify(boosters.get_dict())
    
#Повышение уровня бустера
@bp.route('/boosters/upgrade/<types>/<int:chat_id>', methods=['GET'])
def boosters_upgrade(types, chat_id): 
    boosters: Boosters = Boosters.query.all()[0]
    user: Users = Users.query.filter_by(chat_id=chat_id).first()
    booster_index = boosters.types.index(types)
    
    if user:
        if boosters:
            if user.balance_features >= boosters.prices[booster_index][user.boosters[booster_index+2]]:
                #Покупка нового уровня
                user.balance = user.balance - boosters.prices[booster_index][user.boosters[booster_index+2] + 1]
                user.balance_features = user.balance_features - boosters.prices[booster_index][user.boosters[booster_index+2] + 1]
                new_level = user.boosters.copy()
                new_level[booster_index+2]+=1
                user.boosters = new_level
                db.session.commit()
                return jsonify({'success': True, "balance":new_level})
            else:
                return jsonify({'success': False, "error":"Недостаточно средств"})
        else:
            return jsonify({'success': False, "error":"Бустеры не инициализированы"})
    else:
        return jsonify({'success': False, "error":"Такого пользователя не существует"})
    
#Активация ежедневного бустера
@bp.route('/boosters/activate/<types>/<int:chat_id>', methods=['GET'])
def boosters_activate(types, chat_id):
    xboosters: Xboosters = Xboosters.query.filter_by(user=chat_id).first()
    user: Users = Users.query.filter_by(chat_id=chat_id).first()
    
    b_index = {
        "xrange":0,
        "xleverage":1
    }
    
    if user:
        if user.boosters[b_index[types]] == 0:
            if not xboosters:
                new_boosters = user.boosters.copy()
                new_boosters[b_index[types]] = 1
                user.boosters = new_boosters
                db.session.add(
                    Xboosters(
                        type=types,
                        dateactivate=dt.datetime.now(),
                        active=True,
                        user=chat_id
                    )
                )
                db.session.commit()
                return jsonify({'success': True})
            else:
                check = dt.datetime.now() - dt.datetime.strptime(xboosters.dateactivate, '%Y-%m-%d %H:%M:%S.%f')
                if check.days != 0:
                    xboosters.active = True
                    new_boosters = user.boosters.copy()
                    new_boosters[b_index[types]] = 1
                    user.boosters = new_boosters
                    db.session.commit()
                    return jsonify({'success': True})
                else:
                    return jsonify({'success': False, "error":"Прошло меньше 24 часов", "timeout":86400-check.seconds})
        else:    
            return jsonify({'success': False, "error":"Бустер активен"})
    else:
        return jsonify({'success': False, "error":"Такого пользователя не существует"})
    
#Деактивация ежедневного бустера
@bp.route('/boosters/deactivate/<types>/<int:chat_id>', methods=['GET'])
def boosters_deactivate(types, chat_id):
    xboosters: Xboosters = Xboosters.query.filter_by(user=chat_id).first()
    user: Users = Users.query.filter_by(chat_id=chat_id).first()
    
    b_index = {
        "xrange":0,
        "xleverage":1
    }
    
    if user:
        if user.boosters[b_index[types]] == 1:
            if not xboosters:
                return jsonify({'success': False, "error":"Бустер ненайден"})
            else:
                new_boosters = user.boosters.copy()
                new_boosters[b_index[types]] = 0
                user.boosters = new_boosters
                xboosters.active = False
                db.session.commit()
                return jsonify({'success': True})
        else:    
            return jsonify({'success': False, "error":"Бустер не активен"})
    else:
        return jsonify({'success': False, "error":"Такого пользователя не существует"})