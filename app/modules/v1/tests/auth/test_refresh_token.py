from main import app
from fastapi.testclient import TestClient
from modules.v1.tests.auth.test_login import URL as LOGIN_URL

client = TestClient(app)
URL = "/v1/auth/refresh-token"

EMAIL = "someemail@gmail.com"
PASSWORD = "Pa$$wd123"

def test_success_refresh_token(get_db):
    login_response = client.post(LOGIN_URL, json={
        "email": EMAIL,
        "password": PASSWORD
    })

    response = client.post(URL, json={
        "refreshToken": login_response.json()['refreshToken']
    })
    assert response.status_code == 200
    assert response.json()['accessToken']
    assert response.json()['refreshToken']

def test_failed_refresh_token(get_db):
    response = client.post(URL, json={
        "refreshToken": '372g8fpemdsfdhks'
    })
    assert response.status_code == 401