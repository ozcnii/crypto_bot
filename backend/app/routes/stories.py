from flask import Blueprint, jsonify, request, abort
from app.models import Stories
from app import db
import json
from config import DevelopmentConfig

bp = Blueprint('stories', __name__)

@bp.route('/stories', methods=['GET'])
def stories():
    response = None
    
    #Получение всех историй
    if request.method == "GET":
        response = []
        all_stories = Stories.query.all()
        for stori in all_stories:
            response.append(
                stori.get_dict()
            )
        return jsonify(response)
    
#Получение истории
@bp.route('/stories/<int:ids>', methods=['GET'])
def stories_search(ids):
    response = None
    
    if request.method == "GET":
        try:
            user = Stories.query.filter_by(id=ids).first()
            if user:
                response=user.get_dict()
            else:
                response = {"success":False, "error": "Такой истории не сущесвует"}
        except Exception as error:
            response = {"success":False, "error": str(error)}
            
        return jsonify(response)
    
#Получение актуальных историй
@bp.route('/stories/getnow', methods=['GET'])
def stories_get():
    return None