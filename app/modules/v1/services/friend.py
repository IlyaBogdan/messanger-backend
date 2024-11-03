from typing import List
from sqlalchemy import exc
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException, status

from modules.v1.dto.user import UserBase
from modules.v1.services import user as UserService
from modules.v1.models.user import User, friends_association
from modules.v1.dto.friend import SetFriendRequestStatus, CreateFriendRequest
from modules.v1.models.friend_request import FriendRequest, FriendRequestStatus
    
def add_to_friends(user: User, friend: User, db: Session) -> bool:
    """Add another user to friends

    Parameters
    ----------
    user: User
        User model
    friend: User
        Another user
    db: Session
        Database connection

    Raises
    ------
    HTTPException: 409
        If user already in friend list
    """
    if friend in user.friends:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already in friend list")
    
    user.friends.append(friend)
    friend.friends.append(user)
    db.commit()
    return True

def delete_friend(user: User, friend: User, db: Session) -> bool:
    """Delete another user from friends

    Parameters
    ----------
    user: User
        User model
    friend: User
        Another user
    db: Session
        Database connection

    Raises
    ------
    HTTPException: 409
        If user not in friend list
    """
    if friend not in user.friends:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not in friend list")
    
    user.friends.remove(friend)
    friend.friends.remove(user)
    db.commit()
    return True

def common_friends(user: User, other: User, db: Session) -> List[UserBase]:
    """Return list of common friends for 2 users

    Parameters
    ----------
    user: User
        User model
    other: User
        Another user
    db: Session
        Database connection
    """
    return db.query(User).filter(
        User.id.in_(
            db.query(friends_association.c.friend_id)
            .filter(friends_association.c.user_id == user.id)
            .intersect(
                db.query(friends_association.c.friend_id)
                .filter(friends_association.c.user_id == other.id)
            )
        )
    ).all()

def create_friend_request(data: CreateFriendRequest, user: User, db: Session) -> bool:
    """Create friend request

    Parameters
    ----------
    data: CreateFriendRequest
        Data for friend request creating
    user: User
        Initiator
    db: Session
        Database connection

    Raises
    ------
    HTTPException: 409
        If alredy exists friend request for given users
    """
    try:
        existing_request_for_initiator = db.query(FriendRequest).filter(FriendRequest.initiator_id==user.id, FriendRequest.receiver_id==data.friendId).first()
        if existing_request_for_initiator:
            raise exc.IntegrityError(db, {}, None)
        existing_request_for_reciever = db.query(FriendRequest).filter(FriendRequest.receiver_id==user.id, FriendRequest.initiator_id==data.friendId).first()
        if existing_request_for_reciever:
            raise exc.IntegrityError(db, {}, None)
        
        request = FriendRequest()
        request.receiver = UserService.get_user(data.friendId, db)
        request.initiator = user
        db.add(request)
        db.commit()

        return True

    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Friend request for given users already exists")


def set_friend_request_status(data: SetFriendRequestStatus, user: User, db: Session) -> bool:
    """Set status of friend request

    Parameters
    ----------
    data: SetFriendRequestStatus
        Data for friend request status setting
    user: User
        User model
    db: Session
        Database connection

    Raises
    ------
    HTTPException: 409
        If have no request with taken ID
    """
    request = db.query(FriendRequest).filter(
        FriendRequest.receiver_id==user.id,
        FriendRequest.id==data.requestId
    ).first()
    if request:
        if request.status != data.status:
            request.status = data.status

            if request.status == FriendRequestStatus.APPROVED.value:
                add_to_friends(user, request.initiator, db)

            db.commit()
            return True

    return False