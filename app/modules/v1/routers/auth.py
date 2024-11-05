from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from modules.v1.dto import auth
from modules.v1.services import auth as AuthService

router = APIRouter()

@router.post(
    path='/v1/auth/login',
    tags={"Auth"},
    summary="Login",
    response_model=auth.AuthResponse
)
async def login(data: auth.LoginDto, db: Session = Depends(get_db)):
    return AuthService.login(data, db)

@router.post(
    path='/v1/auth/registration',
    tags={"Auth"},
    summary="Registration",
    response_model=auth.AuthResponse
)
async def registration(data: auth.AuthRequest, db: Session = Depends(get_db)):
    return AuthService.registration(data, db)

@router.post(
    path='/v1/auth/refresh-token',
    tags={"Auth"},
    summary="Refresh JWT token",
    response_model=auth.AuthResponse
)
async def refresh_token(data: auth.RefreshToken, db: Session = Depends(get_db)):
    return AuthService.refresh_token(data, db)

@router.post(
    path='/v1/auth/password/init-reset',
    tags={"ResetPassword"},
    summary="Init reset password process",
    response_model=dict
)
async def init_reset_password(data: auth.ResetPasswordInit, db: Session = Depends(get_db)):
    return { "success": AuthService.init_reset_password(data, db) }

@router.post(
    path='/v1/auth/password/change',
    tags={"ResetPassword"},
    summary="Change password",
    response_model=dict
)
async def change_password(data: auth.ChangePassword, db: Session = Depends(get_db)):
    return { "success": AuthService.change_password(data, db) }