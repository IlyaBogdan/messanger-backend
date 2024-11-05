from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
URL = "/v1/friends/common"

OTHER_USER = 2
NOT_EXISTING_USER = 99999999

def test_common_friend_list_successfully_accepted(access_token_1):
    response = client.get(URL, params={
        'user_id': OTHER_USER
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 200

def test_try_get_common_friends_with_not_existed_user(access_token_1):
    response = client.get(URL, params={
        'user_id': NOT_EXISTING_USER
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 404
    assert response.json()['detail'] == f'User with id {NOT_EXISTING_USER} not found'
