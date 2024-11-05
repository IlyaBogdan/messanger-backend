import pytest

from database import get_db
from modules.v1.models.user import User
from modules.v1.services.auth import get_password_hash, authorize

@pytest.fixture(scope="session", autouse=True)
def register_users():
    users = [
        User(email="someemail@gmail.com", password=get_password_hash("Pa$$wd123"), username="Billi Herington"),
        User(email="someemail1@gmail.com", password=get_password_hash("Pa$$wd123"), username="Van Darkholme"),
        User(email="someemail2@gmail.com", password=get_password_hash("Pa$$wd123"), username="Peter Parker"),
        User(email="someemail3@gmail.com", password=get_password_hash("Pa$$wd123"), username="Bruce Wayne"),
        User(email="someemail4@gmail.com", password=get_password_hash("Pa$$wd123"), username="Joe Biden", is_deleted=True),

        User(email="someemail6@gmail.com", password=get_password_hash("Pa$$wd123"), username="John Snow"),
        User(email="someemail7@gmail.com", password=get_password_hash("Pa$$wd123"), username="Harley Queen"),
        User(email="someemail8@gmail.com", password=get_password_hash("Pa$$wd123"), username="Big Smoke", is_deleted=False),
        User(email="someemail9@gmail.com", password=get_password_hash("Pa$$wd123"), username="Carl Jonson"),
        User(email="someemail10@gmail.com", password=get_password_hash("Pa$$wd123"), username="Conor Kanwey"),
        
        User(email="someemail11@gmail.com", password=get_password_hash("Pa$$wd123"), username="Desmond Miles"),
        User(email="someemail12@gmail.com", password=get_password_hash("Pa$$wd123"), username="Codlac Gray", is_deleted=False),
        User(email="someemail13@gmail.com", password=get_password_hash("Pa$$wd123"), username="Nikola Tesla"),
        User(email="someemail14@gmail.com", password=get_password_hash("Pa$$wd123"), username="Isaak Newton"),
        User(email="someemail15@gmail.com", password=get_password_hash("Pa$$wd123"), username="Horus Luperkal"),
    ]

    db = next(get_db())
    for user in users:
        db.add(user)
    db.commit()

@pytest.fixture(scope="session")
def access_token_1():
    db = next(get_db())
    user = db.query(User).filter(User.id == 1).first()
    return authorize(user).accessToken

@pytest.fixture(scope="session")
def access_token_2():
    db = next(get_db())
    user = db.query(User).filter(User.id == 2).first()
    return authorize(user).accessToken