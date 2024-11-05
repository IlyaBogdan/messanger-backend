from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
URL = "/v1/auth/login"

EMAIL = "someemail@gmail.com"
DELETED_USER_EMAIL = "someemail4@gmail.com"
PASSWORD = "Pa$$wd123"
INVALID_PASSWORD = "parapssda"

def test_success_login():
    response = client.post(URL, json={
        "email": EMAIL,
        "password": PASSWORD
    })
    assert response.status_code == 200
    assert response.json()['accessToken']
    assert response.json()['refreshToken']

def test_failed_login():
    response = client.post(URL, json={
        "email": EMAIL,
        "password": INVALID_PASSWORD
    })
    assert response.status_code == 401
    assert response.json()['detail'] == "Incorrect username or password"

def test_login_if_user_deleted():
    response = client.post(URL, json={
        "email": DELETED_USER_EMAIL,
        "password": PASSWORD
    })
    assert response.status_code == 401
    assert response.json()['detail'] == "Incorrect username or password"