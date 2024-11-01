from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from modules.v1.models.user import User
from modules.v1.dto.user import UserBase

def get_user(id: int, db: Session) -> Optional[User]:
    """Get info about user by ID

    Parameters
    ----------
    id: int
        User's ID
    db: Session
        Database connection
    """
    return db.query(User).filter(User.id==id).first()


def update(data: UserBase, db: Session) -> Optional[User]:
    """Update user info
    
    Parameters
    ----------
    data: UserBase
        User's information
    db: Session
        Database connection
    """
    user = get_user(data.id, db)
    if user:
        user.name = data.name
        user.email = data.email
        db.commit()
        db.refresh(user)

    return user

def remove(id: int, db: Session) -> Optional[User]:
    """Remove user using soft delete

    Parameters
    ----------
    data: UserBase
        User's information
    db: Session
        Database connection
    """
    user = get_user(id, db)
    if user:
        user.is_deleted = True
        db.commit()
        db.refresh(user)
        return user
    
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