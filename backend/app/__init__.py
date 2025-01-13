from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Создаем объект SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Users, Stories, Orders, Boosters, Clans
from app.routes.user import bp as userRoute
from app.routes.stories import bp as storiesRoute
from app.routes.orders import bp as ordersRoute
from app.routes.boosters import bp as boostersRoute
from app.routes.clans import bp as clansRoute

#routes
app.register_blueprint(userRoute)
app.register_blueprint(storiesRoute)
app.register_blueprint(ordersRoute)
app.register_blueprint(boostersRoute)
app.register_blueprint(clansRoute)
