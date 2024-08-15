from datetime import datetime
import pytz
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base_model import DataBase

def moscow_time():
    return datetime.now(pytz.timezone('Europe/Moscow'))

class Users(DataBase):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    username = Column(String)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=True)
    clan_id = Column(Integer, ForeignKey('clans.id'))  # ID клана, к которому принадлежит пользователь
    token = Column(String)
    role = Column(String, default="User")
    blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=moscow_time)
    balance = Column(Integer, default=0)
    p_n_l = Column(Integer, default=0)
    power = Column(Integer, default=10)
    avatar_url = Column(String, nullable=True)
    
    # RELATIONSHIP
    clan = relationship("Clans", back_populates="members", foreign_keys=[clan_id])
    owned_clans = relationship("Clans", back_populates="owner", foreign_keys=[clan_id])
    league = relationship("League", back_populates="users", foreign_keys=[league_id])