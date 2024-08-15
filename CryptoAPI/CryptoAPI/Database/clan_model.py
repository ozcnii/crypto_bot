from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import pytz
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import DataBase

class Clans(DataBase):
    __tablename__ = "clans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    link = Column(String)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=True)
    balance = Column(Integer, default=0)
    users = Column(Integer, default=0)
    logo_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))  # ID владельца клана
    
    # RELATIONSHIP
    owner = relationship("Users", back_populates="owned_clans", foreign_keys=[owner_id])
    members = relationship("Users", back_populates="clan", foreign_keys=[owner_id])
    league = relationship("League", back_populates="clans", foreign_keys=[league_id])