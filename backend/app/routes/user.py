from flask import Blueprint, jsonify, request
from app.models import Users
from app import db, getTokenUser, getToken, responseError, responseSuccess, DevelopmentConfig, auth_required
import json
from telebot import TeleBot
from PIL import Image
import hashlib
import io

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['GET', 'POST', 'DELETE', 'PUT'])
@auth_required
def users():
    #Получение пользователя
    if request.method == "GET":
        user: Users = db.session.query(Users).filter(Users.token == getToken(request)).first()
        return jsonify(user.get_dict())
    
    #Добавление пользователя
    if request.method == "POST":
        
        #Обработка данных
        data = json.loads(request.data.decode('utf-8'))
        user = Users(**data)
        bot = TeleBot(DevelopmentConfig.TOKEN)
        
        #Проверка на существование пользователя
        if not Users.query.filter_by(chat_id=user.chat_id).first() and not Users.query.filter_by(username=user.username).first():
            
            #Добавление пользователя
            file = bot.download_file(bot.get_file(bot.get_user_profile_photos(user.chat_id).photos[0][0].file_id).file_path)
            file_path = f'app/static/{hashlib.sha256(str(user.username).encode()).hexdigest()}.jpg'
            Image.open(io.BytesIO(file)).save(file_path)
            photo = file_path.replace('app/','')            
            user.balance_features=user.balance
            user.token = getTokenUser(user.chat_id, user.username)
            user.photo = photo
            db.session.add(user)
            db.session.commit()
            return jsonify(responseSuccess())
            
        else:
            return jsonify(responseError("Такой пользователь уже сущесвует")), 500
            
    #Удаление пользователя
    if request.method == "DELETE":
        
        #Поиск пользователя
        user = Users.query.filter(Users.token==getToken(request)).first()
        
        #Удаление
        db.session.delete(user)
        db.session.commit()
        return jsonify(responseSuccess())
    
    #Обновление информации о пользователе
    if request.method == "PUT":
        
        #Обработка данных
        data = json.loads(request.data.decode('utf-8'))
        user = Users.query.filter(Users.token==getToken(request)).first()
        
        #Обновление информации
        try:
            for param in data.keys():
                setattr(user, param, data[param])
        except:
            return jsonify(responseError("Ошибка: неверные данные")), 500
        
        db.session.commit()
        return jsonify(responseSuccess())
        
@bp.route('/users/getreflink', methods=['GET'])
@auth_required
def users_getreflink():
    #Полезная нагрузка
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    return jsonify(responseSuccess(reflink=f'{DevelopmentConfig.BOTLINK}?start={user.chat_id}'))

#Добавление реферала
@bp.route('/users/addref', methods=['POST'])
@auth_required
def users_addref():
    #Обработка данных
    data = json.loads(request.data.decode('utf-8'))
    
    if 'ref_id' not in data and "admin_chat_id" not in data:
        return responseError("Неверные данные"), 500
    
    try:
        int(data["admin_chat_id"])
    except:
        return responseError("Неверные данные"), 500
        
    
    user: Users = Users.query.filter(Users.chat_id==int(data["admin_chat_id"])).first()
    
    if user.referals != [] and user.referals!=None:
        if data['ref_id'] in user.referals:
            return responseError("Такой пользователь уже приглашён"), 500
    
    if user.referals!=[] and user.referals!=None:
        l_ref = user.referals.copy()
        l_ref.append(data['ref_id'])
        user.referals=l_ref
    else:
        user.referals=[data['ref_id']]
    
    if data['premium']:
        user.balance_features = user.balance_features + 100
        user.balance = user.balance + 100
        user.sum_ref = user.sum_ref + 100
    else:
        user.balance_features = user.balance_features + 1000
        user.balance = user.balance + 1000
        user.sum_ref = user.sum_ref + 1000
        
    #Сохранить
    db.session.commit()
    
    return jsonify(responseSuccess())

#Добавление получение списка рефералов
@bp.route('/users/getref', methods=['GET'])
@auth_required
def users_getref():
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    response = []
    
    for user_ref_id in user.referals:
        user_ref: Users = Users.query.filter(Users.chat_id==user_ref_id).first()
        if user_ref.premium == 1:
            response.append((user_ref.balance, 1000, user_ref.username, user.photo))
        else:
            response.append((user_ref.balance, 100, user_ref.username, user.photo)) 
                       
    return jsonify(responseSuccess(ref_list=response))
        

#Кнопка TOPLEADER 300
@bp.route('/users/topleader', methods=['GET'])
@auth_required
def users_topleader():
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    all_users = Users.query.all()
    sort_top_list_users = sorted([(len(x.referals) if x.referals!=None else 0 , x.sum_ref, x.photo) for x in all_users], key=lambda x: x[0], reverse=True)
    my_place = sort_top_list_users.index((len(user.referals) if user.referals!=None else 0, user.sum_ref, user.photo)) + 1
    
    if len(sort_top_list_users) > 300:
        sort_top_list_users = sort_top_list_users[0:300]
        
    return jsonify(responseSuccess(
        my_place_number=my_place,
        top_300_leader=sort_top_list_users
    ))
    
@bp.after_request
def allow_everyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response