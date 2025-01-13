from flask import Blueprint, jsonify, request, abort
from app.models import Orders, Users
from app import db
import json
from config import DevelopmentConfig
import datetime as dt

bp = Blueprint('orders', __name__)

#Получить все ордеры
@bp.route('/orders', methods=['GET'])
def orders():
    response = None
    
    if request.method == "GET":
        response = []
        all_stories = Orders.query.all()
        for stori in all_stories:
            response.append(
                stori.get_dict()
            )
        return jsonify(response)
    
#Создать ордер
@bp.route('/orders/open/<int:chat_id>', methods=['POST'])
def open_orders(chat_id):
    data = json.loads(request.data.decode())
    user: Users = Users.query.filter_by(chat_id=chat_id).first()
    # print(user)
    # print(' -> ',chat_id, data)
    
    if 'priceinput' in data and\
        'amount' in data and\
        'position' in data and\
        'leverage' in data and\
        'symbol' in data and\
        user != None:
        
        order: Orders = Orders(
            **data
        )
        
        #Добавление тейков
        if 'tp' in data:
            if data['tp'] <= order.priceinput and order.position == 'long':
                return jsonify({
                    "success":False,
                    "error":"TP Должен быть выше текущего значения цены"
                })                   
            elif data['tp'] >= order.priceinput and order.position == 'short':
                return jsonify({
                    "success":False,
                    "error":"TP Должен быть ниже текущего значения цены"
                })  
            else:
                order.tp = data['tp']
        if 'sl' in data:
            if data['sl'] >= order.priceinput and order.position == 'long':
                return jsonify({
                    "success":False,
                    "error":"SL Должен быть ниже текущего значения цены"
                })                   
            elif data['sl'] <= order.priceinput and order.position == 'short':
                return jsonify({
                    "success":False,
                    "error":"sl Должен быть выше текущего значения цены"
                })  
            else:
                order.sl = data['sl'] 
        
        #Корректировка
        order.user = chat_id
        order.dateinput = dt.datetime.now()
        order.active = True
        order.pnl = 0.0
        
        if user.balance_features - order.amount < 0: return jsonify({"success":False, "error":"Недостаточно средств"})
        else:user.balance_features = user.balance_features - order.amount
        
        if not user.trades:
            user.trades = [len(Orders.query.all())+1]
        else:
            user.trades = [*user.trades, len(Orders.query.all())+1]
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({'success': True, 'order_id':order.id})
    
    else:
        return jsonify({'success': False, 'error':"Некорректный запрос"})
        # Цена ликвидации = (цена входа × размер позиции + маржа) ÷ (размер позиции × (1 – ставка поддерживающей маржи))
        
#Обновить ордер
@bp.route('/orders/update/<int:id>', methods=['POST'])
def update_orders(id):
    data = json.loads(request.data.decode())
    order: Orders = Orders.query.filter_by(id=id).first()
    
    if order:
        if 'coinprice' in data:
            if order.active:
                user: Users = Users.query.filter_by(chat_id=order.user).first()
                
                #Добавление тейков
                if 'tp' in data:
                    if data['tp'] <= data['coinprice'] and order.position == 'long':
                        return jsonify({
                            "success":False,
                            "error":"TP Должен быть выше текущего значения цены"
                        })                   
                    elif data['tp'] >= data['coinprice'] and order.position == 'short':
                        return jsonify({
                            "success":False,
                            "error":"TP Должен быть ниже текущего значения цены"
                        })  
                    else:
                        order.tp = data['tp']
                if 'sl' in data:
                    if data['sl'] >= data['coinprice'] and order.position == 'long':
                        return jsonify({
                            "success":False,
                            "error":"SL Должен быть ниже текущего значения цены"
                        })                   
                    elif data['sl'] <= data['coinprice'] and order.position == 'short':
                        return jsonify({
                            "success":False,
                            "error":"SL Должен быть выше текущего значения цены"
                        })  
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
                
                if order.active == False:
                    order.dateoutput = dt.datetime.now()
                
                db.session.commit()
                
                return jsonify({
                    "success":True,
                    "order":order.get_dict()
                })
            else:
                return jsonify({
                    "success":False,
                    "error":"Ордер закрыт"
                })                     
            
        else:
            return jsonify({
                "success":False,
                "error":"Текущая цена не указана"
            })            
        
        
    else:
        return jsonify({
            "success":False,
            "error":"Такого ордера не существует"
        })
        