from flask import Blueprint, jsonify, request
from app.models import Users, Clans
from app import db, responseError, responseSuccess, getToken, auth_required

bp = Blueprint('league', __name__)

#Отображение лиги
@bp.route('/league', methods=['GET'])
@auth_required
def league():
    #Обработка данных
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    
    #Проверка лиг пользователей   
    all_player_list = Users.query.all()
    for other_user in all_player_list:
        if other_user.balance < 100000.0:
            other_user.league = 'bronze'
        elif other_user.balance > 100000.0 and other_user.balance < 1000000.0:
            other_user.league = 'silver'
        elif other_user.balance > 1000000.0 and other_user.balance < 10000000.0:
            other_user.league = 'golden'
        elif other_user.balance > 100000000.0:
            other_user.league = 'diamond'        
    
    #Сохраняем информацию
    db.session.commit()
    
    #Подсчёт игроков, опеределение места в лиге
    list_league = Users.query.filter(Users.league==user.league).all()
    list_league_balance = [(x.balance, x.username) for x in list_league]
    sort_list_league_balance = sorted(list_league_balance, key=lambda x: x[0], reverse=True)
    response_list_league_player = [{"username": x[1], "balance": x[0]} for x in sort_list_league_balance]
    my_palce = sort_list_league_balance.index((user.balance, user.username)) + 1
    count_player = len(sort_list_league_balance)
    count_all_player = len(all_player_list)
    
    return jsonify(responseSuccess(
        list_league=response_list_league_player,
        me_place_number=my_palce,
        count_this_league_player=count_player,
        count_all_player=count_all_player
    ))
    
#Отображение конкретной лиги
@bp.route('/league/<league>', methods=['GET'])
@auth_required
def league_other_get(league):
    #Проверка данных
    if league in ['bronze', 'silver', 'golden', 'diamond']: 
        
        #Подсчё пользователей  
        list_league_users=Users.query.filter(Users.league==league).all()
        if list_league_users!=[]:
            sorted_list_league_player = sorted([(x.balance, x.username) for x in list_league_users], key=lambda x: x[0])
            return jsonify(responseSuccess(list_league_player=sorted_list_league_player))
    else:
        return jsonify(responseError("Неверные данные")), 500

#Лиги кланов
@bp.route('/league/clan', methods=['GET'])
@auth_required
def league_clan():
    #Обработка данных
    user: Users = Users.query.filter(Users.token==getToken(request)).filter()
    clan: Clans = Clans.query.filter(Clans.peer==user.clan).filter()
    
    #Проверка лиг пользователей   
    all_clan_list = Clans.query.all()
    for other_clan in all_clan_list:
        if other_clan.balance < 100000.0:
            other_clan.league = 'bronze'
        elif other_clan.balance > 100000.0 and other_clan.balance < 1000000.0:
            other_clan.league = 'silver'
        elif other_clan.balance > 1000000.0 and other_clan.balance < 10000000.0:
            other_clan.league = 'golden'
        elif other_clan.balance > 100000000.0:
            other_clan.league = 'diamond'
            
    #Сохранение данных
    db.session.commit()
    
    #Проверка на существование клана
    if clan:
        list_clan_this_league = [(x.balance, x.photo, x.name) for x in Clans.query.filter(Clans.league==clan.league).all()]
        sort_list_clan_this_league = sorted(list_clan_this_league, key=lambda x: x[0])
        me_clan_place = sort_list_clan_this_league.index((clan.balance, clan.photo, clan.name)) + 1
        all_clan_player = len(clan.users)
        all_clan_this_league = len(list_clan_this_league)
        return jsonify(responseSuccess(
            me_clan_place=me_clan_place,
            all_clan_player=all_clan_player,
            all_clan_this_league_count=all_clan_this_league,
            list_clan_this_league=sort_list_clan_this_league
        ))
    else:
        return jsonify(responseError("Пользователь не в клане, но данные обновлены")), 500

#Лиги кланов
@bp.route('/league/clan/<league>', methods=['GET'])
@auth_required
def league_clan_league_get(league):
    #Проверка данных
    if league in ['bronze', 'silver', 'golden', 'diamond']: 
        
        #Обработка данных
        all_clan_this_league = Clans.query.filter(Clans.league==league).all()
        if all_clan_this_league!=[]:
            sorted_all_clan_this_league=sorted([(x.balance, x.photo, x.name) for x in all_clan_this_league], key=lambda x: x[0])
            return jsonify(responseSuccess(all_clan_this_league=sorted_all_clan_this_league))
    else:
        return jsonify(responseError("Неверные данные")), 500

@bp.after_request
def allow_everyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response