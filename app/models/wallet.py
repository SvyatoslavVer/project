from sqlalchemy import Column, String, Integer
from app.core.db import Base

class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)