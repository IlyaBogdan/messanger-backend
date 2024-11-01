from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from modules.v1.services import user as UserService
from modules.v1.dto.user import UserBase, UserCreate

router = APIRouter()

@router.post(
    path='/v1/user/',
    tags={"User"},
    summary="Create new user",
    response_model=UserCreate
)
async def create(data: UserCreate = None, db: Session = Depends(get_db)):
    return UserService.create_user(data, db)

@router.get(
    path='/v1/user/{id}',
    tags={"User"},
    summary="Get user by ID",
    response_model=UserBase
)
async def get(id: int, db: Session = Depends(get_db)):
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
async def update(id: int, data: UserBase = None, db: Session = Depends(get_db)):
    user = UserService.update(data, id, db)
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.delete(
    path='/v1/user/{id}',
    tags={"User"},
    summary="Remove user by ID",
    description="Soft removal is used",
    response_model=UserBase
)
async def delete(id: int, db: Session = Depends(get_db)):
    user = UserService.remove(id, db)
    if user:
        return user

    raise HTTPException(status_code=404, detail=f"User with id {id} not found")