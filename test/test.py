from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_wallet():
    response = client.post("/wallets/", json={"id": 1,"address": "0x59354356ec5d56306791873f567d61ebf11dfbd5"})
    assert response.status_code == 200
    assert response.json()["address"] == "0x1234"

def test_add_token():
    response = client.post("/tokens/", json={"id": 0, "symbol": "ETH", "contract_address": "0x5678"})
    assert response.status_code == 200
    assert response.json()["symbol"] == "ETH"
