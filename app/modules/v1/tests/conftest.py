import pytest
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from modules.v1.models.user import User
from modules.v1.services.auth import get_password_hash

@pytest.fixture(scope="session", autouse=True)
def register_users():
    users = [
        User(email="someemail@gmail.com", password=get_password_hash("Pa$$wd123")),
        User(email="someemail1@gmail.com", password=get_password_hash("Pa$$wd123")),
        User(email="someemail2@gmail.com", password=get_password_hash("Pa$$wd123")),
        User(email="someemail3@gmail.com", password=get_password_hash("Pa$$wd123")),
        User(email="someemail4@gmail.com", password=get_password_hash("Pa$$wd123"), is_deleted=True),
    ]

    db = next(get_db())
    for user in users:
        db.add(user)
    db.commit()