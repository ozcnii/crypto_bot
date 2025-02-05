from flask import Blueprint, jsonify, request
from app.models import Boosters, Users, Xboosters
from app import db, getToken, checkAuth, responseError, auth_required
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
        return jsonify(responseError("Бустеры не инициализированы")),500
    else:
        return jsonify({'success': True})
    
#Вернуть все бустеры
@bp.route('/boosters/getall', methods=['GET'])
def boosters_get_all(): 
    boosters: Boosters = Boosters.query.all()
    
    if boosters == []:
        return jsonify(responseError("Бустеры не инициализированы")), 500
    else:
        return jsonify(boosters.get_dict())
    
#Повышение уровня бустера
@bp.route('/boosters/upgrade/<types>', methods=['GET'])
@auth_required
def boosters_upgrade(types): 
    
    #Обработка данных
    boosters: Boosters = Boosters.query.all()[0]
    user: Users = Users.query.filter(Users.token == getToken(request)).first()
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
                return jsonify({'success': True})
            else:
                return jsonify(responseError("Недостаточно средств")),500
        else:
            return jsonify(responseError("Бустеры не инициализированы")),500
    else:
        return jsonify(responseError("Такого пользователя не существует")),500
    
#Активация ежедневного бустера
@bp.route('/boosters/activate/<types>', methods=['GET'])
@auth_required
def boosters_activate(types):
    
    #Обработка данных
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    xboosters: Xboosters = Xboosters.query.filter_by(user=user.chat_id).first()
    b_index = {"xrange":0,"xleverage":1}
    
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
                return jsonify(responseError(f"Прошло меньше 24 часов timeout: {86400-check.seconds}")),500
    else:    
        return jsonify(responseError("Бустер активен")),500
    
#Деактивация ежедневного бустера
@bp.route('/boosters/deactivate/<types>', methods=['GET'])
@auth_required
def boosters_deactivate(types):
    
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    xboosters: Xboosters = Xboosters.query.filter_by(user=user.chat_id).first()
    
    b_index = {
        "xrange":0,
        "xleverage":1
    }
    
    if user.boosters[b_index[types]] == 1:
        if not xboosters:
            return jsonify(responseError("Бустер не найден")),500
        else:
            new_boosters = user.boosters.copy()
            new_boosters[b_index[types]] = 0
            user.boosters = new_boosters
            xboosters.active = False
            db.session.commit()
            return jsonify({'success': True})
    else:    
        return jsonify(responseError("Бустер не активен")),500
    
@bp.after_request
def allow_everyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response