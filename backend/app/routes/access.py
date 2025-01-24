from flask import Blueprint, jsonify, request, abort
from app.models import Users
from app import db, app
import jwt
import json

bp = Blueprint('jwtauth', __name__)

@bp.route('/auth', methods=['POST'])
def auth():
    data = json.loads(request.data.decode('utf-8'))
    
    if "id" not in data or "username" not in data:
        return jsonify({'success': False, "error":"Неверные данные"}), 500
        
    playload = {
        "id": data["id"],
        "username":data["username"]
    }
    
    #Подпись токена
    token = jwt.encode(playload, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'access_token': token})
