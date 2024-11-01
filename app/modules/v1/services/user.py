from typing import Optional
from sqlalchemy.orm import Session

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
        db.add(user)
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
    """
    user.friends.append(friend)
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
    """
    user.friends.remove(friend)
    db.commit()
    return True