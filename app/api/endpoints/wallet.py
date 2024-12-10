from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.core.db import get_db
from pydantic import BaseModel

router = APIRouter()

class WalletCreate(BaseModel):
    address: str

@router.post("/")
def add_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = Wallet(address=wallet.address)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

@router.delete("/{wallet_id}")
def delete_wallet(wallet_id: int, db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if db_wallet:
        db.delete(db_wallet)
        db.commit()
        return {"msg": "Wallet deleted"}
    return {"msg": "Wallet not found"}
