import sys

from apscheduler.schedulers.background import BackgroundScheduler
from app.models.wallet import Wallet
from app.models.token import Token
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from fastapi import HTTPException
from web3 import Web3
from pydantic import BaseModel

class BalanceResponse(BaseModel):
    wallet: str
    balance: int

def collect_balances():
    db = SessionLocal()
    wallets = db.query(Wallet).all()
    tokens = db.query(Token).all()
    w3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))

    for wallet in wallets:
        for token in tokens:
            # Логика получения баланса для каждого токена на кошельке
            wallet = db.query(Wallet).filter(Wallet.id == wallet.id).first()
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet not found")

            # Используем Web3 для получения баланса токенов
            balance = w3.eth.get_balance(wallet.address)
            balance = BalanceResponse(wallet=wallet.address, balance=balance)

            sys.stderr.write(f"Wallet: {wallet.address}, Token: {token.address}, Balance: {balance}")

scheduler = BackgroundScheduler()
scheduler.add_job(collect_balances, 'interval', seconds=10)
scheduler.start()
