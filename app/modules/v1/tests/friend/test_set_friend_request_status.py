from main import app
from fastapi.testclient import TestClient

from modules.v1.models.friend_request import FriendRequestStatus

client = TestClient(app)
URL = "/v1/friends/friends-request/set-status"

EXISTED_REQUEST = 3
NOT_EXISTED_REQUEST = 999999

def test_status_successfully_changed(access_token_1):
    response = client.post(URL, json={
        'requestId': EXISTED_REQUEST,
        'status': FriendRequestStatus.APPROVED
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 200
    assert response.json()['success']

def test_try_set_status_not_existed_request(access_token_1):
    response = client.post(URL, json={
        'requestId': NOT_EXISTED_REQUEST,
        'status': FriendRequestStatus.APPROVED
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 404
    assert response.json()['detail'] == 'Friend request not found'

def test_try_to_set_same_status(access_token_1):
    response = client.post(URL, json={
        'requestId': EXISTED_REQUEST,
        'status': FriendRequestStatus.APPROVED
    }, headers={
       'Authorization': f'Bearer {access_token_1}' 
    })
    assert response.status_code == 409
    assert response.json()['detail'] == 'Request already has this status'
