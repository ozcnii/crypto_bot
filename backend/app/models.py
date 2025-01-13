from app import db
'''
flask migration ->

flask db migrate -m "<comment>"
flask db upgrade

'''
class Clans(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    peer = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Integer, nullable=False)
    users = db.Column(db.JSON, nullable=False)
    league = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Clans {self.id}>'    
    
    def get_dict(self):
        return{
            "id":self.id,
            "peer":self.peer,
            "admin":self.admin,
            "users":self.users,
            "league":self.league,
            "name":self.name,
        }

class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    lifetime = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(128), nullable=False)
    adddata = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Stories {self.id}>'    
    
    def get_dict(self):
        return{
            "id": self.id,
            "lifetime": self.lifetime,
            "photo": self.photo,
            "adddata":self.adddata
        }
        
class Boosters(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    types = db.Column(db.JSON, nullable=False)
    prices = db.Column(db.JSON, nullable=False)
    profits = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f'<Boosters {self.id}>'    
    
    def get_dict(self):
        return{
            "id": self.id,
            "types": self.types,
            "prices": self.prices,
            "profits":self.profits
        }
        
class Xboosters(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    type = db.Column(db.String(64), nullable=False)
    dateactivate = db.Column(db.String(64),nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    user = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Xboosters {self.id}>'    
    
    def get_dict(self):
        return{
            "id": self.id,
            "type": self.type,
            "dateactivate": self.dateactivate,
            "active":self.active,
            "user":self.user
        }
        
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    symbol = db.Column(db.String(64))
    priceinput = db.Column(db.Float)
    amount = db.Column(db.Float)
    pnl = db.Column(db.Float)
    position = db.Column(db.String(64),nullable=False)
    leverage = db.Column(db.Integer,nullable=False)
    user = db.Column(db.Integer,nullable=False)
    dateinput = db.Column(db.String(64),nullable=False)
    dateoutput = db.Column(db.String(64))
    active = db.Column(db.Boolean, nullable=False)
    tp = db.Column(db.Float)
    sl = db.Column(db.Float)
    liquidation = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Orders {self.id}>'    
    
    def get_dict(self):
        return{
            'id':self.id,
            'symbol':self.symbol,
            'priceinput':self.priceinput,
            'amount':self.amount,
            'pnl':self.pnl,
            'position':self.position,
            'leverage':self.leverage,
            'user':self.user,
            'dateinput':self.dateinput,
            'dateoutput':self.dateoutput,
            'active':self.active,
            'tp':self.tp,
            'sl':self.sl,
            'liquidation':self.liquidation,
        }
    
class Users(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    balance_features = db.Column(db.Float)
    league = db.Column(db.String(128), nullable=False)
    pnl = db.Column(db.Float)
    trades = db.Column(db.JSON)
    boosters = db.Column(db.JSON)
    clan = db.Column(db.Integer)
    tasks = db.Column(db.JSON)
    referals = db.Column(db.JSON)
    historycheck = db.Column(db.JSON)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_dict(self):
        return{
            "chat_id" : self.chat_id,
            "username" : self.username,
            "balance" : self.balance,
            "balance_features" : self.balance_features,
            "league" : self.league,
            "pnl" : self.pnl,
            "trades" : self.trades,
            "boosters" : self.boosters,
            "clan" : self.clan,
            "tasks" : self.tasks,
            "referals" : self.referals,
            "historycheck" : self.historycheck,
        }