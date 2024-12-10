from celery import Celery
from web3 import Web3
from app.models.wallet import Wallet
from app.models.token import Token
from app.core.db import SessionLocal

app3 = Celery('balance_collector', broker='redis://redis:6379/0', result_backend='redis://redis:6379/0',include=['app.core.task'])


@app3.task
def collect_balances():
    db = SessionLocal()
    wallets = db.query(Wallet).all()
    tokens = db.query(Token).all()
    w3 = Web3(Web3.HTTPProvider('https://arb1.arbitrum.io/rpc'))
    #print("TEST")
    for wallet in wallets:
        for token in tokens:
            # Получаем баланс для каждого токена на кошельке
            #contract = w3.eth.contract(address=token.contract_address, abi=[...])  # Нужно указать ABI токена
            #balance = contract.functions.balanceOf(wallet.address).call()
            balance = w3.eth.get_balance(w3.to_checksum_address(wallet.address))
            #print("TEST")
            print(f"Balance for {wallet.address} in {token.symbol}: {balance}")
            #write to db ???
            #print({"balance": w3.from_wei(balance, token.symbol)}

    db.close()

app3.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'app.core.task.collect_balances',
        'schedule': 10.0
    }
}