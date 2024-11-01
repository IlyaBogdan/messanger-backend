from sqlalchemy.orm import Session
from typing import Optional
from modules.v1.models.user import User
from modules.v1.dto.user import UserCreate, UserBase

def create_user(data: UserCreate, db: Session) -> User:
    user = User(name=data.name)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return user

def get_user(id: int, db: Session) -> Optional[User]:
    return db.query(User).filter(User.id==id).first()


def update(data: UserBase, id: int, db: Session) -> Optional[User]:
    user = get_user(id, db)
    if user:
        user.name = data.name
        db.add(user)
        db.commit()
        db.refresh(user)

    return user

def remove(id: int, db: Session) -> Optional[User]:
    user = get_user(id, db)
    if user:
        user.is_deleted = True
        db.commit()
        db.refresh(user)
        return user