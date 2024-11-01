import jwt
import uuid
from os import environ
from sqlalchemy import exc
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Request, Depends

from modules.v1.dto import chat
from modules.v1.models.chat import Chat
from modules.v1.models.user import User
from modules.v1.services import user as UserService

def create_new_chat(data: chat.ChatBase, db: Session) -> Chat:
    """Create new user chat

    Parameters
    ----------
    data: chat.ChatBase
        Info for chat creating
    db: Session
        Database connection
    """
    pass

def get_user_chat(id: int, user: User, db: Session) -> Chat:
    """Return user chat by ID

    Parameters
    ----------
    id: int
        User chat ID
    user: User
        User info
    db: Session
        Database connection
    """
    pass

def remove_user_chat(id: int, db: Session) -> Chat:
    """Remove user chat by ID

    Parameters
    ----------
    id: int
        User chat ID
    db: Session
        Database connection
    """
    pass

def update_user_chat(data: chat.ChatBase, db: Session) -> Chat:
    """Update user chat info

    Parameters
    ----------
    data: chat.ChatBase
        Chat info
    db: Session
        Database connection
    """
    pass
