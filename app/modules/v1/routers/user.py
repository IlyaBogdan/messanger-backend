from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException

from modules.v1.models.user import User
from modules.v1.dto.user import UserBase, AddFriend
from modules.v1.services import user as UserService
from modules.v1.services import auth as AuthService

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

@router.get(
    path='/v1/user/friends/get-all',
    tags={"UserFriends"},
    summary="Get user friends",
    response_model=List[UserBase]
)
async def friends(
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    return user.friends

@router.post(
    path='/v1/user/friends/add-friend',
    tags={"UserFriends"},
    summary="Add user to friends",
    response_model=dict
)
async def add_to_friends(
    data: AddFriend,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    if data.friend_id != user.id:
        friend = UserService.get_user(data.friend_id, db)
        if not friend:
            raise HTTPException(status_code=404, detail=f"User with id {data.friend_id} not found")
        
        return { "success": UserService.add_to_friends(user, friend, db) }

@router.delete(
    path='/v1/user/friends/delete-friend',
    tags={"UserFriends"},
    summary="Delete user from friend list",
    response_model=dict
)
async def delete_friend(
    data: AddFriend,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    if data.friend_id != user.id:
        friend = UserService.get_user(data.friend_id, db)
        if not friend:
            raise HTTPException(status_code=404, detail=f"User with id {data.friend_id} not found")
        
        return { "success": UserService.delete_friend(user, friend, db) }