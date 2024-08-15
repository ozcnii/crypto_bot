from enum import Enum
from sqlalchemy import Column, Integer, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base_model import DataBase

class LeagueName(str, Enum):
  BRONZE = 'Bronze'
  SILVER = 'Silver'
  GOLD = 'Gold'
  DIAMOND = 'Diamond'

class League(DataBase):
  __tablename__ = "leagues"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(SQLAEnum(LeagueName), index=True, unique=True)
  user_count = Column(Integer, default=0)
  clan_count = Column(Integer, default=0)
  
  users = relationship("User", back_populates="league")
  
  clans = relationship("Clan", back_populates="league")
  