from app import app
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory

#Настройки swagger
@app.route('/swaggerdoc/<path>')
def send_static(path):
    return send_from_directory('swaggerdoc', path)

SWAGGER_URL = '/swagger'
API_URL = '/swaggerdoc/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Aenolabs Docs"
    }
)