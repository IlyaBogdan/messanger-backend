from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from modules.v1.services import user as UserService
from modules.v1.dto import user as UserDto

router = APIRouter()

@router.post(
    path='/v1/user/',
    tags={"User"},
    summary="Create new user",
    response_model=UserDto.User
)
async def create(data: UserDto.User = None, db: Session = Depends(get_db)):
    return UserService.create_user(data, db)

@router.get(
    path='/v1/user/{id}',
    tags={"User"},
    summary="Get user by ID",
    response_model=UserDto.User
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
    response_model=UserDto.User
)
async def update(id: int, data: UserDto.User = None, db: Session = Depends(get_db)):
    user = UserService.update(data, id, db)
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.delete(
    path='/v1/user/{id}',
    tags={"User"},
    summary="Remove user by ID",
    description="Soft removal is used",
    response_model=UserDto.User
)
async def delete(id: int, db: Session = Depends(get_db)):
    user = UserService.remove(id, db)
    if user:
        return user

    raise HTTPException(status_code=404, detail=f"User with id {id} not found")