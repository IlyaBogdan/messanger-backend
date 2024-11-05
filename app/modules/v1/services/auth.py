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

from modules.v1.dto import auth
from database import get_db
from modules.v1.models.user import User
from modules.v1.services import user as UserService
from modules.v1.models.reset_token import ResetToken


SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(environ.get("REFRESH_TOKEN_EXPIRE_DAYS"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db: Session) -> User:
    """Verify access token

    Parameters
    ----------
    token: str
        User's access token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Get user in current request

    Parameters
    ----------
    request: Request
        Current request instance
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    print(auth_header)
    scheme, token = auth_header.split()
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")

    user = verify_token(token, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return user

def authorize(user: User) -> auth.AuthResponse:
    """User authorization

    Parameters
    ----------
    user: User
        User for authorization
    """

    access_token = create_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        data={"sub": user.email}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return auth.AuthResponse(accessToken=access_token, refreshToken=refresh_token)

def login(data: auth.LoginDto, db: Session) -> Optional[auth.AuthResponse]:
    """Method for user login

    Check user credentionals and authorize him

    Parameters
    ----------
    data: auth.LoginDto
        User's email and plain password
    db: Session
        Database connection

    Raises
    ------
    HTTPException: 401
        If user with given email or password not exists

    """
    user = db.query(User).filter(User.email == data.email, User.is_deleted == False).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return authorize(user)


def registration(data: auth.AuthRequest, db: Session) -> Optional[auth.AuthResponse]:
    """Method for user registration

    Register new user and authorize him

    Parameters
    ----------
    data: auth.AuthRequest
        User's email and plain password
    db: Session
        Database connection

    Raises
    ------
    HTTPException: 409
        If user with given email already exists

    """
    user = User()
    user.email = data.email
    user.password = get_password_hash(data.password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return authorize(user)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {data.email} already exists")

def refresh_token(data: auth.RefreshToken, db: Session) -> auth.AuthResponse:
    """Refresh expired access token

    Parameters
    ----------
    data: auth.RefreshToken
        User's refresh token
    db: Session
        Database connection

    Raises
    ------
    HTTPException: 409
        If user with given email already exists

    """
    try:
        payload = jwt.decode(data.refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return auth.AuthResponse(accessToken=access_token, refreshToken=data.refreshToken)

def init_reset_password(data: auth.ResetPasswordInit, db: Session) -> bool:
    """Init reset password process
    Sends reset password link to email

    Parameters
    ----------
    data: auth.ResetPasswordInit
        User's email
    db: Session
        Database connection
    """
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        reset_token = ResetToken()
        reset_token.user_id = user.id
        reset_token.expired_date = datetime.now(timezone.utc) + timedelta(days=1)
        reset_token.token = uuid.uuid4()
        db.add(reset_token)
        db.commit()
        db.refresh(reset_token)

        # TODO: send link to email

    return True
    
def change_password(data: auth.ChangePassword, db: Session) -> bool:
    """Change current user password

    Parameters
    ----------
    data: auth.ChangePassword
        New user's password
    db: Session
        Database connection
    """
    reset_token = db.query(ResetToken).filter(ResetToken.token == data.resetToken).first()
    if reset_token:
        user = UserService.get_user(reset_token.user_id, db)
        user.password = get_password_hash(data.newPassword)
        db.delete(reset_token)
        for token in db.query(ResetToken).filter(ResetToken.user_id == user.id).all():
            db.delete(token)

        db.commit()

    return True