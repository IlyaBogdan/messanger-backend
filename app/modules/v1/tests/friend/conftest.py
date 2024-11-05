import pytest

from database import get_db
from modules.v1.services.user import get_user
from modules.v1.services.friend import add_to_friends
from modules.v1.models.friend_request import FriendRequest, FriendRequestStatus

@pytest.fixture(scope="session", autouse=True)
def init_friend_list():
    db = next(get_db())
    user = get_user(1, db)
    add_to_friends(user, get_user(3, db), db)
    add_to_friends(user, get_user(4, db), db)

    user = get_user(2, db)
    add_to_friends(user, get_user(3, db), db)
    add_to_friends(user, get_user(5, db), db)

@pytest.fixture(scope="session", autouse=True)
def init_friend_requests():
    friend_requests = [
        FriendRequest(initiator_id=3, receiver_id=1, status=FriendRequestStatus.APPROVED),
        FriendRequest(initiator_id=1, receiver_id=4, status=FriendRequestStatus.APPROVED),
        FriendRequest(initiator_id=6, receiver_id=1, status=FriendRequestStatus.WAITING),
        FriendRequest(initiator_id=1, receiver_id=7, status=FriendRequestStatus.REJECTED),

        FriendRequest(initiator_id=2, receiver_id=6, status=FriendRequestStatus.WAITING),
    ]

    db = next(get_db())
    for friend_request in friend_requests:
        db.add(friend_request)
    db.commit()