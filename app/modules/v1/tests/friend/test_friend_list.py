from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
URL = "/v1/friends/"

def test_friend_list_successfully_accepted(access_token_1):
    response = client.get(URL, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 200
