from flask import Blueprint, jsonify, request
from app.models import Orders, Users
from app import db, getToken, responseError, auth_required, check_week_date
import json
import datetime as dt

bp = Blueprint('orders', __name__)

#Получить все ордеры пользователя
@bp.route('/orders', methods=['GET'])
@auth_required
def orders():
    #Полезная нагрузка
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    all_orders = Orders.query.filter(Orders.user==user.chat_id).all()
    return jsonify([x.get_dict() for x in all_orders]) 

#Недельный pnl
@bp.route('/orders/getweekpnl', methods=['GET'])
@auth_required
def order_pnl_week():
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    
    try:
        all_pnl = [x.pnl for x in Orders.query.filter(Orders.user==user.chat_id).all() if check_week_date(x.dateoutput)]
        pnl = round(sum(all_pnl)/len(all_pnl), 2)
        user.pnl = pnl
        
        db.session.commit()
    except ZeroDivisionError:
        return jsonify(responseError("Нулевой pnl")), 500
    
    return jsonify({"pnl": pnl})
 
#Создать ордер
@bp.route('/orders/open', methods=['POST'])
@auth_required
def open_orders():
    #Обработка данных
    data = json.loads(request.data.decode())
    user: Users = Users.query.filter(Users.token==getToken(request)).first()
    
    if 'priceinput' in data and\
        'amount' in data and\
        'position' in data and\
        'leverage' in data and\
        'symbol' in data and\
        user != None:
        
        #Создание объекта ордера
        order: Orders = Orders(**data)
        
        #Добавление тейков
        if 'tp' in data:
            if data['tp'] <= order.priceinput and order.position == 'long':
                return jsonify(responseError("TP Должен быть выше текущего значения цены")), 500     
            elif data['tp'] >= order.priceinput and order.position == 'short':
                return jsonify(responseError("TP Должен быть ниже текущего значения цены")), 500
            else:
                order.tp = data['tp']
        if 'sl' in data:
            if data['sl'] >= order.priceinput and order.position == 'long':
                return jsonify(responseError("SL Должен быть ниже текущего значения цены")), 500                 
            elif data['sl'] <= order.priceinput and order.position == 'short':
                return jsonify(responseError("SL Должен быть выше текущего значения цены")), 500
            else:
                order.sl = data['sl'] 
        
        #Корректировка
        order.user = user.chat_id
        order.dateinput = dt.datetime.now()
        order.active = True
        order.pnl = 0.0
        
        if user.balance_features - order.amount < 0:
            return jsonify(responseError("Недостаточно средств")), 500
        else:
            user.balance_features = user.balance_features - order.amount
        
        if not user.trades:
            user.trades = [len(Orders.query.all())+1]
        else:
            user.trades = [*user.trades, len(Orders.query.all())+1]
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({'success': True, 'order_id':order.id})
    
    else:
        return jsonify(responseError("Некорректный запрос")), 500
        # Цена ликвидации = (цена входа × размер позиции + маржа) ÷ (размер позиции × (1 – ставка поддерживающей маржи))
        
#Обновить ордер
@bp.route('/orders/update/<int:id>', methods=['POST'])
@auth_required
def update_orders(id):
    #Обработка данных
    data = json.loads(request.data.decode())
    order: Orders = Orders.query.filter_by(id=id).first()
    
    if order:
        #Проверка доступа
        user: Users = Users.query.filter(Users.token==getToken(request)).first()
        if order.id not in user.trades:
            return jsonify(responseError("Отказано в доступе")), 503
        
        if 'coinprice' in data:
            if order.active:
                #Добавление тейков
                if 'tp' in data:
                    if data['tp'] <= data['coinprice'] and order.position == 'long': 
                        return jsonify(responseError("TP Должен быть выше текущего значения цены")), 500       
                    elif data['tp'] >= data['coinprice'] and order.position == 'short':
                        return jsonify(responseError("TP Должен быть ниже текущего значения цены")), 500
                    else:
                        order.tp = data['tp']
                if 'sl' in data:
                    if data['sl'] >= data['coinprice'] and order.position == 'long':
                        return jsonify(responseError("SL Должен быть ниже текущего значения цены")),500                  
                    elif data['sl'] <= data['coinprice'] and order.position == 'short':
                        return jsonify(responseError("SL Должен быть выше текущего значения цены")), 500 
                    else:
                        order.sl = data['sl']          
            
                user.balance = user.balance - (((order.amount/100)*order.pnl)+order.amount)
                
                #Формула PNL
                nowAmountCoin = data['coinprice']*order.amount
                inputAmountCoin = order.priceinput*order.amount
                procent = (nowAmountCoin-inputAmountCoin)/100
                order.pnl = (procent * 100)*order.leverage
                
                if order.position == "long":
                    order.liquidation = ((order.priceinput*order.amount)*order.leverage-100)/order.amount
                else:
                    order.liquidation = ((order.priceinput*order.amount)*order.leverage+100)/order.amount
                
                if order.position != "long":
                    order.pnl = order.pnl *-1
                    
                #Конверт в деньги
                user.balance = user.balance + (((order.amount/100)*order.pnl)+order.amount)
                    
                #TL/SL
                if order.position == "long" and order.tp:
                    if data['coinprice'] >= order.tp:
                        order.active = False
                        user.balance_features = user.balance_features + (((order.amount/100)*order.pnl)+order.amount)
                if order.position == "long" and order.sl:
                    if data['coinprice'] <= order.sl:
                        order.active = False
                        user.balance_features = user.balance_features + (((order.amount/100)*order.pnl)+order.amount)
                if order.position == "short" and order.sl:
                    if data['coinprice'] >= order.sl:
                        order.active = False
                        user.balance_features = user.balance_features + (((order.amount/100)*order.pnl)+order.amount)
                if order.position == "short" and order.tp:
                    if data['coinprice'] <= order.tp:
                        order.active = False
                        user.balance_features = user.balance_features + (((order.amount/100)*order.pnl)+order.amount)                    

                #Ликвидация
                if order.pnl <= -100.0:
                    order.active = False
                    user.balance_features = user.balance_features + (((order.amount/100)*order.pnl)+order.amount)
                
                if 'active' in data:
                    if data['active'] == False:
                        order.active = False
                
                if order.active == False:
                    order.dateoutput = dt.datetime.now()
                
                db.session.commit()
                
                return jsonify({"success":True,"order":order.get_dict()})
            else:
                return jsonify(responseError("Ордер закрыт")), 500                   
        else:
            return jsonify(responseError("Текущая цена не указана")), 500
    else:
        return jsonify(responseError("Такого ордера не существует")), 500
        
@bp.after_request
def allow_everyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response
        