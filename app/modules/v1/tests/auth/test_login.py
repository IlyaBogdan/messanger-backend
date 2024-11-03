from main import app
from fastapi.testclient import TestClient

from database import get_db

client = TestClient(app)

def test_success_login(get_db):
    response = client.post("/v1/auth/login", {
        "email": "someemail@gmail.com",
        "password": "Pa$$wd123"
    })
    assert response.status_code == 200
    assert response.json()