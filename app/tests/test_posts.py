import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_201(monkeypatch):
    payload = {"username": "test_user_x", "email": "test_user_x@test.com", "posts": 0}
    r = client.post("/users", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert "id" in body and body["id"] > 0
    assert body["username"] == "test_user_x"

def test_create_user_conflict_email():
    # criar primeiro
    client.post("/users", json={"username":"dup1","email":"dup@test.com","posts":0})
    # tentar criar com mesmo email (username diferente)
    r = client.post("/users", json={"username":"dup2","email":"dup@test.com","posts":0})
    assert r.status_code == 409
    assert r.json()["detail"] == "Email already exists"

def test_create_user_conflict_username():
    # criar primeiro
    client.post("/users", json={"username":"dupname","email":"dupname@test.com","posts":0})
    # tentar criar com mesmo username (email diferente)
    r = client.post("/users", json={"username":"dupname","email":"dupname2@test.com","posts":0})
    assert r.status_code == 409
    assert r.json()["detail"] == "Username already exists"
