from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
URL = "/v1/friends/friend-request"

FRIEND_IN_LIST_ID = 3
FRIEND_ID = 2
DELETED_FRIEND = 5

def test_friend_request_successfully_created(access_token_1):
    response = client.post(URL, json={
        'friendId': FRIEND_ID
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 200
    assert response.json()['success']

def test_try_add_deleted_user_to_friends(access_token_1):
    response = client.post(URL, json={
        'friendId': DELETED_FRIEND
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 404
    assert response.json()['detail'] == f'User with id {DELETED_FRIEND} not found'

def test_try_to_add_to_friends_already_added_user(access_token_1):
    response = client.post(URL, json={
        'friendId': FRIEND_IN_LIST_ID
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 409
    assert response.json()['detail'] == f'User with id {FRIEND_IN_LIST_ID} already your friend'

def test_try_to_add_to_friend_with_already_created_request(access_token_1):
    response = client.post(URL, json={
        'friendId': FRIEND_ID
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 409
    assert response.json()['detail'] == 'Friend request for given users already exists'

def test_recent_test_from_another_side(access_token_2):
    response = client.post(URL, json={
        'friendId': 1
    }, headers={
       'Authorization': f'Bearer {access_token_2}' 
    })
    assert response.status_code == 409
    assert response.json()['detail'] == 'Friend request for given users already exists'