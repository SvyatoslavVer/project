from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.token import Token
from app.core.db import get_db
from pydantic import BaseModel

router2 = APIRouter()

class TokenCreate(BaseModel):
    symbol: str
    contract_address: str

@router2.post("/")
def add_token(token: TokenCreate, db: Session = Depends(get_db)):
    db_token = Token(symbol=token.symbol, contract_address=token.contract_address)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

@router2.delete("/{token_id}")
def delete_token(token_id: int, db: Session = Depends(get_db)):
    db_token = db.query(Token).filter(Token.id == token_id).first()
    if db_token:
        db.delete(db_token)
        db.commit()
        return {"msg": "Token deleted"}
    return {"msg": "Token not found"}
