from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from modules.v1.dto.user import UserBase
from modules.v1.models.user import User, friends_association
    
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