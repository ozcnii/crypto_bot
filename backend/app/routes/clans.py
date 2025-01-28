from flask import Blueprint, jsonify, request
from app.models import Users, Clans, Orders
from app import db, responseError, responseSuccess, Struct, getToken, auth_required, check_day_date
import json
from config import DevelopmentConfig
from telebot import TeleBot
from PIL import Image
import hashlib
import io

bp = Blueprint('clans', __name__)

#Работа с кланами
@bp.route('/clans', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_required
def clans(): 
    #Получение списка всех кланов
    if request.method == "GET":
        
        #Обновление баланса кланов
        for clan in Clans.query.all():
            balance = 0
            for user_id in clan.users:
                user = Users.query.filter(Users.chat_id==user_id).first()
                if user:
                    balance+=user.balance
            clan.balance = balance
            
        db.session.commit()
        return jsonify([x.get_dict() for x in Clans.query.all()])
    
    #Создание клана
    if request.method == "POST":
        
        #Обработка данных
        data = Struct(**json.loads(request.data.decode()))
        user: Users = Users.query.filter(Users.token==getToken(request)).first()
        bot = TeleBot(DevelopmentConfig.TOKEN)
        
        #Собираем информацию о клане
        try:
            channel = bot.get_chat(data.link.replace('https://t.me/','@'))
            file = bot.download_file(bot.get_file(channel.photo.small_file_id).file_path)
            file_path = f'app/static/{hashlib.sha256(str(user.chat_id).encode()).hexdigest()}.jpg'
            Image.open(io.BytesIO(file)).save(file_path)
            photo = file_path.replace('app/','')
            name = channel.title
            peer = channel.id
        except:
            return jsonify(responseError("Не удалось собрать информацию о клане")), 500
        
        #Проверка перед добавлением
        if not Clans.query.filter(Clans.peer==peer).first():
            if not user.clan:
                
                #Добавляем клан
                db.session.add(Clans(
                    peer=peer,
                    admin=user.chat_id,
                    users=[user.chat_id],
                    league='bronze',
                    name=name,
                    balance=user.balance,
                    photo=photo
                ))
                
                user.clan = peer
                db.session.commit()
                return jsonify(responseSuccess())
            else:
                return jsonify(responseError("Пользователь уже в клане")), 500
        else:
            return jsonify(responseError("Такой клан уже существует")), 500
        
    #Удаление клана
    if request.method == "DELETE":
        #Обработка данных
        data = Struct(**json.loads(request.data.decode()))
        user = Users.query.filter(Users.token==getToken(request)).first()       
        clan: Clans = Clans.query.filter_by(peer=data.peer).first()

        if clan:
            if clan.admin == user.chat_id:
                for member_id in clan.users:
                    
                    #Удаление клана у участников
                    clan_member: Users = Users.query.filter(Users.clan==member_id).first()
                    clan_member.clan = None
                    
                #Удаление клана
                db.session.remove(clan)
                db.session.commit()
                
                return jsonify(responseSuccess())
            else:
                return jsonify(responseError("Отказано в доступе")), 503
        else:
            return jsonify(responseError("Такого клана не существует")), 500
                    
        
#Добавление участника в клан
@bp.route('/clans/addmember/<peer>', methods=['GET'])
@auth_required
def clansAddMember(peer):    
    #Обработка данных
    clan: Clans = Clans.query.filter_by(peer=peer).first()
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    
    if not user.clan:
        if clan:
            if user.chat_id not in clan.users:
                nowUsersList = clan.users.copy()
                nowUsersList.append(user.chat_id)
                clan.users = nowUsersList
                user.clan=clan.peer
                db.session.commit()
                return jsonify(responseSuccess())
            else:
                return jsonify(responseError("Пользователь уже добавлен в этот канал")),500
        else:
            return jsonify(responseError("Такого клана не существует")),500
    else:
        return jsonify(responseError("Пользователь уже в клане")),500
    
#Удаление участника из клана
@bp.route('/clans/delmember/<peer>', methods=['GET'])
@auth_required
def clansDelMember(peer):
    #Обработка данных
    clan: Clans = Clans.query.filter_by(peer=peer).first()
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    
    if user.clan is not None:
        if clan:
            if user.chat_id in clan.users:
                nowUsersList = clan.users.copy()
                nowUsersList.remove(user.chat_id)
                user.clan=None
                clan.users = nowUsersList
                db.session.commit()
                return jsonify(responseSuccess())
            else:
                return jsonify(responseError("Пользователя нет в этом клане")),500     
        else:
            return jsonify(responseError("Такого клана не существует")),500
    else:
        return jsonify(responseError("Пользователь не состоит в клане")),500   

#Получение конкретного клана
@bp.route('/clans/me', methods=['GET'])
@auth_required
def clansGet():
    #Обработка данных
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    clan: Clans = Clans.query.filter(Clans.peer==user.clan).first()
        
    if clan:
        
        #Обновление баланса клана
        balance = 0
        for user_id in clan.users:
            user = Users.query.filter(Users.chat_id==user_id).first()
            if user:
                balance += user.balance
        clan.balance = balance
        db.session.commit()
                
        return jsonify(clan.get_dict())
    else:
        return jsonify(responseError("Пользователь не состоит в клане")),500

@bp.route('/clans/dayleader', methods=['GET'])
@auth_required
def clansGetDayLeader():
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    clan: Clans = Clans.query.filter(Clans.peer==user.clan).first()
    list_leader = []
    
    if clan:
        users_clan: list[Users] = Users.query.filter(Users.clan==clan.peer).all()
        day_orders = Orders.query.filter(Orders.user==users_clan)
        me_data = None
        for us_clan in users_clan:
            pnl_list = [x.pnl for x in Orders.query.filter(Orders.user==us_clan.chat_id).all() if check_day_date(x.dateoutput)]
            try:
                pnl = sum(pnl_list)/len(pnl_list)
            except ZeroDivisionError:
                pnl = 0
            list_leader.append((pnl, us_clan.balance, us_clan.username, us_clan.photo))
            if user.username == us_clan.username:
                me_data = (pnl, us_clan.balance, us_clan.username, us_clan.photo)
                
        sort_list_leader = sorted(list_leader, key=lambda x: x[0])
        my_place = sort_list_leader.index(me_data) + 1
        return jsonify(responseSuccess(
            list_day_leader=sort_list_leader,
            my_place=my_place
        ))
    else:
        return jsonify(responseError("У пользователя нет клана")), 500


@bp.route('/clans/alltimeleader', methods=['GET'])
@auth_required
def clansGetAllTimeLeader():
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    clan: Clans = Clans.query.filter(Clans.peer==user.clan).first()
    
    if clan:
        users_clan: list[Users] = Users.query.filter(Users.clan==clan.peer).all()
        sort_list_alltime_leader = sorted([(x.balance, x.username, x.photo) for x in users_clan], key=lambda x: x[0])
        my_place = sort_list_alltime_leader.index(((user.balance, user.username, user.photo))) + 1
        
        return jsonify(responseSuccess(
            list_alltime_leader=sort_list_alltime_leader,
            my_place=my_place
        ))
    else:
        return jsonify(responseError("У пользователя нет клана")), 500

@bp.after_request
def allow_everyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response