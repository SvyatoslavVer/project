from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.token import Token
from app.models.wallet import Wallet
from app.api.endpoints.token import router2
from app.api.endpoints.wallet import router
import web3

app = FastAPI()
#app.include_router(router)
#app.include_router(router2)
# Модели данных для Pydantic
class TokenCreate(BaseModel):
    id: int
    symbol: str
    contract_address: str

class WalletCreate(BaseModel):
    id: int
    address: str

class BalanceResponse(BaseModel):
    wallet: str
    balance: int

# Функции для работы с базой данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tokens/")
async def add_token(token: TokenCreate, db: Session = Depends(get_db)):
    db_token = db.query(Token).filter(Token.contract_address == token.contract_address).first()
    if db_token:
        raise HTTPException(status_code=400, detail="Token already exists")
    db_token = Token(**token.model_dump())
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

@app.delete("/tokens/{contract_address}")
async def delete_token(contract_address: str, db: Session = Depends(get_db)):
    db_token = db.query(Token).filter(Token.contract_address == contract_address).first()
    if db_token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    db.delete(db_token)
    db.commit()
    return {"message": "Token deleted successfully"}

@app.post("/wallets/")
async def add_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.address == wallet.address).first()
    if db_wallet:
        raise HTTPException(status_code=400, detail="Wallet already exists")
    db_wallet = Wallet(**wallet.model_dump())
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

@app.delete("/wallets/{address}")
async def delete_wallet(address: str, db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.address == address).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    db.delete(db_wallet)
    db.commit()
    return {"message": "Wallet deleted successfully"}

@app.get("/balances/{wallet_address,token}")
async def get_balance(wallet_address: str,token: str, db: Session = Depends(get_db)):
    db_wallet = db.query(Wallet).filter(Wallet.address == wallet_address).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    # Взаимодействие с blockchain для получения баланса
    # Пример с Arbitrum (к примеру, подключение через RPC)
    w3 = web3.Web3(web3.Web3.HTTPProvider("https://arb1.arbitrum.io/rpc"))
    balance = w3.eth.get_balance(w3.to_checksum_address(wallet_address))
    return {"balance": w3.from_wei(balance, token)}
