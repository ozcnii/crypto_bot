from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLAEnum, Float, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from enum import Enum
from datetime import datetime
import pytz
from Database import DataBase

class LeagueName(str, Enum):
    BRONZE = 'Bronze'
    SILVER = 'Silver'
    GOLD = 'Gold'
    DIAMOND = 'Diamond'

class League(DataBase):
    __tablename__ = "leagues"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(SQLAEnum(LeagueName), index=True, unique=True)
    user_count = Column(Integer, default=0, nullable=False)
    clan_count = Column(Integer, default=0, nullable=False)
  
    users = relationship("Users", back_populates="league")
    clans = relationship("Clans", back_populates="league")

class Users(DataBase):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    username = Column(String)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False, default=1)
    clan_id = Column(Integer, ForeignKey('clans.id'), nullable=True)  # ID клана, к которому принадлежит пользователь
    token = Column(String)
    role = Column(String, default="User")
    blocked = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(pytz.timezone('Europe/Moscow')))
    balance = Column(Integer, default=100)
    p_n_l = Column(Integer, default=0)
    power = Column(Integer, default=10)
    avatar_url = Column(String, nullable=True)
    referral_code = Column(String, unique=True)  # Код для приглашения других пользователей
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # ID пользователя, который пригласил этого пользователя
    is_premium = Column(Boolean, default=False)
    
    # RELATIONSHIPS
    clan = relationship("Clans", back_populates="members", foreign_keys=[clan_id])
    owned_clans = relationship("Clans", back_populates='owner', foreign_keys='Clans.owner_id')
    league = relationship("League", back_populates="users", foreign_keys=[league_id])
    referrer = relationship("Users", remote_side=[id])  # Связь с пользователем, который пригласил этого пользователя
    user_tasks = relationship("UserTask", back_populates="user")
    open_orders = relationship("Order", back_populates="user")
    boosters = relationship("Boosters", back_populates="user")
    
class Order(DataBase):
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contract_pair = Column(String)  # Trading pair like TON/USD
    entry_rate = Column(Float)  # Entry rate at the time of order creation
    exit_rate = Column(Float, nullable=True)  # Exit rate when order is closed
    amount = Column(Float)  # Amount in MainCoin
    direction = Column(String)  # "long" or "short"
    leverage = Column(Integer, default=1)  # Leverage (default is 1x, meaning no leverage)
    status = Column(String, default="open")  # "open", "closed", "pending"
    pnl_value = Column(Float, default=0)
    pnl_percentage = Column(Float, default=0)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(pytz.timezone('Europe/Moscow')))
    closed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # RELATIONSHIPS
    user = relationship("Users", back_populates="open_orders", foreign_keys=[user_id])

class Clans(DataBase):
    __tablename__ = "clans"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    link = Column(String)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False, default=1)
    balance = Column(Integer, default=0)
    users = Column(Integer)
    logo_url = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    # RELATIONSHIPS
    members = relationship("Users", back_populates="clan", foreign_keys='Users.clan_id')
    owner = relationship('Users', back_populates='owned_clans', foreign_keys=[owner_id])
    league = relationship("League", back_populates="clans")
    
    async def update_balance(self):
        total_balance = sum(member.balance for member in self.members)
        self.balance = total_balance
    
class Referrals(DataBase):
    __tablename__ = "referrals"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID пользователя, который пригласил
    referred_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID приглашенного пользователя
    is_premium = Column(Boolean, default=False)  # Является ли приглашенный пользователем Telegram Premium
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(pytz.timezone('Europe/Moscow')))

class UserTask(DataBase):
    __tablename__ = "user_tasks"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID пользователя
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)  # ID задания
    progress = Column(Integer, default=0, nullable=False)  # Прогресс выполнения задания
    completed = Column(Boolean, default=False)  # Выполнено ли задание
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(pytz.timezone('Europe/Moscow')))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(pytz.timezone('Europe/Moscow')), onupdate=datetime.now(pytz.timezone('Europe/Moscow')))
    
    user = relationship("Users", back_populates="user_tasks")
    task = relationship("Task", back_populates="user_tasks")
    
class TaskType(str, Enum):
    EARN_COINS = "earn_coins"
    INVITE_FRIENDS = "invite_friends"
    JOIN_SQUAD = "join_squad"

class Task(DataBase):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название задания
    type = Column(SQLAEnum(TaskType), nullable=False)  # Тип задания
    description = Column(String, nullable=True)  # Описание задания
    target_value = Column(Integer, nullable=False)  # Целевое значение для выполнения задания (например, 1000 коинов или 10 друзей)
    reward = Column(Integer, nullable=False)  # Награда за выполнение задания
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(pytz.timezone('Europe/Moscow')))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(pytz.timezone('Europe/Moscow')), onupdate=datetime.now(pytz.timezone('Europe/Moscow')))
    
    user_tasks = relationship("UserTask", back_populates="task")
    
class Boosters(DataBase):
    __tablename__ = "boosters"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID пользователя
    range_lvl = Column(Integer, nullable=False, default=1)
    leverage_lvl = Column(Integer, nullable=False, default=1)
    trades_lvl = Column(Integer, nullable=False, default=1)
    
    turbo_range_uses = Column(Integer, default=3)
    turbo_range_active = Column(Boolean, default=False)
    x_leverage_uses = Column(Integer, default=3)
    x_leverage_active = Column(Boolean, default=False)
    last_reset = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone('Europe/Moscow')))
    
    user = relationship("Users", back_populates="boosters")

class BoosterType(str, Enum):
    RANGE = "range"
    LEVERAGE = "leverage"
    TRADES = "trades"

class BoosterPrices(DataBase):
    __tablename__ = "booster_prices"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    booster_type = Column(SQLAEnum(BoosterType), nullable=False)
    level = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

class BoosterEffects(DataBase):
    __tablename__ = "booster_effects"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    booster_type = Column(SQLAEnum(BoosterType), nullable=False)
    level = Column(Integer, nullable=False)
    effect_value = Column(DECIMAL(10, 2), nullable=False, default=0.00)

class VerificationCodes(DataBase):
  __tablename__ = "verify_codes"
  __table_args__ = {'extend_existing': True}
  # ROOT
  id = Column(Integer, primary_key=True, index=True)
  
  # USER DATA
  user_email = Column(String)
  user_code = Column(Integer)
  verify_code = Column(Boolean, default=False)
  
class VerificationRestoreCodes(DataBase):
  __tablename__ = "verify_restore_codes"
  __table_args__ = {'extend_existing': True}
  # ROOT
  id = Column(Integer, primary_key=True, index=True)
  
  # USER DATA
  user_email = Column(String)
  user_code = Column(Integer)
  verify_code = Column(Boolean, default=False)