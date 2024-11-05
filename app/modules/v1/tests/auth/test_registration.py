from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
URL = "/v1/auth/registration"

def test_success_registration(get_db):
    print(get_db)
    # response = client.post(URL, json={
    #     "email": "someemail@gmail.com",
    #     "password": "Pa$$wd123"
    # })
    # assert response.status_code == 200
    # assert response.json()

def test_failed_registration(get_db):
    print(get_db)

    # response = client.post(URL, json={
    #     "email": "someemail@gmail.com",
    #     "password": "Pa$$wd123"
    # })
    # assert response.status_code == 401
    # assert response.json()['detail'] == "Incorrect username or password"