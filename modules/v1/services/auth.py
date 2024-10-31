from sqlalchemy.orm import Session

from modules.v1.dto import auth

def login(data: auth.AuthRequest, db: Session) -> auth.AuthResponse:
    pass

def registration(data: auth.AuthRequest, db: Session) -> auth.AuthResponse:
    pass

def refresh_token(data: auth.RefreshToken, db: Session) -> auth.AuthResponse:
    pass