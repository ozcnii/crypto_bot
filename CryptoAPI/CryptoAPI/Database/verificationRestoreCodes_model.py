from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from .base_model import DataBase

class VerificationRestoreCodes(DataBase):
  __tablename__ = "verify_restore_codes"
  
  # ROOT
  id = Column(Integer, primary_key=True, index=True)
  
  # USER DATA
  user_email = Column(String)
  user_code = Column(Integer)
  verify_code = Column(Boolean, default=False)