from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_unauthorized_user_info():
    response = client.get("/v1/user/1")
    assert response.status_code == 401