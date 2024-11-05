from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
URL = "/v1/friends/"

FRIEND_IN_LIST_ID = 3
FRIEND_NOT_IN_LIST_ID = 10
NOT_EXISTING_USER = 99999999
DELETED_FRIEND = 5

def test_friend_successfully_deleted(access_token_1):
    response = client.delete(URL + str(FRIEND_IN_LIST_ID), headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 200
    assert response.json()['success']

def test_try_delete_not_existed_user(access_token_1):
    response = client.delete(URL + str(NOT_EXISTING_USER), headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 404
    assert response.json()['detail'] == f'User with id {NOT_EXISTING_USER} not found'

def test_try_delete_not_existed_in_friend_list_user(access_token_1):
    response = client.delete(URL + str(FRIEND_NOT_IN_LIST_ID), headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 409
    assert response.json()['detail'] == f'User not in friend list'
