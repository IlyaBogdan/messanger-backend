from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException

from modules.v1.dto.user import UserBase
from modules.v1.services import user as UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")
router = APIRouter()    

@router.get(
    path='/v1/user/{id}',
    tags={"User"},
    summary="Get user by ID",
    response_model=UserBase
)
async def get(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = UserService.get_user(id, db)
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.put(
    path='/v1/user/{id}',
    tags={"User"},
    summary="Change user info",
    response_model=UserBase
)
async def update(
    data: UserBase,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = UserService.update(data, db)
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User with id {data.id} not found")

@router.delete(
    path='/v1/user/{id}',
    tags={"User"},
    summary="Remove user by ID",
    description="Soft removal is used",
    response_model=UserBase
)
async def delete(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = UserService.remove(id, db)
    if user:
        return user

    raise HTTPException(status_code=404, detail=f"User with id {id} not found")
