import hashlib
from fastapi import HTTPException
from sqlalchemy import exc
from typing import Optional
from sqlalchemy.orm import Session
from modules.v1.dto import auth
from modules.v1.models.user import User

def authorize(user: User) -> auth.AuthResponse:
    auth_data = auth.AuthResponse(accessToken="asdasdas", refreshToken="sadasata")
    return auth_data

def login(data: auth.AuthRequest, db: Session) -> Optional[auth.AuthResponse]:
    email = data.email
    password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    user = db.query(User).filter(User.email==email, User.password==password, User.is_deleted==False).first()
    if user:
        return authorize(user)
    raise HTTPException(status_code=401, detail="Invalid email or password")

def registration(data: auth.AuthRequest, db: Session) -> Optional[auth.AuthResponse]:
    user = User()
    user.email = data.email
    user.password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return authorize(user)
    except exc.IntegrityError:
        raise HTTPException(status_code=409, detail=f"User with email {data.email} already exists")

def refresh_token(data: auth.RefreshToken, db: Session) -> auth.AuthResponse:
    auth_data = auth.AuthResponse(accessToken="asdasdas", refreshToken="sadasata")
    return auth_data