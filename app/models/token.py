from sqlalchemy import Column, String, Integer
#from app.core.db import Base
from app.core.db import Base
class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    contract_address = Column(String, unique=True, index=True)
    # blockchain
    # Blockchain table -> list of tokens