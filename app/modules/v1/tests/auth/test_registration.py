from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
URL = "/v1/auth/registration"

VALID_EMAIL = "someemail5@gmail.com"
VALID_PASSWORD = "Pa$$wd123"
INVALID_EMAIL = "someemai"
INVALID_PASSWORD = "Paer352"

def test_success_registration():
    response = client.post(URL, json={
        "email": VALID_EMAIL,
        "password": VALID_PASSWORD
    })
    assert response.status_code == 200
    assert response.status_code == 200
    assert response.json()['accessToken']
    assert response.json()['refreshToken']

def test_user_already_exists():
    response = client.post(URL, json={
        "email": VALID_EMAIL,
        "password": VALID_PASSWORD
    })
    assert response.status_code == 409
    assert response.json()['detail'] == f"User with email {VALID_EMAIL} already exists"

def test_invalid_email():
    response = client.post(URL, json={
        "email": INVALID_EMAIL,
        "password": VALID_PASSWORD
    })
    assert response.status_code == 422

def test_invalid_password():
    response = client.post(URL, json={
        "email": VALID_EMAIL,
        "password": INVALID_PASSWORD
    })
    assert response.status_code == 422