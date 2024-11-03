from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException

from modules.v1.models.user import User
from modules.v1.dto.user import UserBase, AddFriend
from modules.v1.services import user as UserService
from modules.v1.services import auth as AuthService
from modules.v1.services import friend as FriendService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")
router = APIRouter()    

@router.get(
    path='/v1/friends',
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
    path='/v1/friends/add',
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
        
        return { "success": FriendService.add_to_friends(user, friend, db) }

@router.delete(
    path='/v1/friends/{friend_id}',
    tags={"UserFriends"},
    summary="Delete user from friend list",
    response_model=dict
)
async def delete_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    if friend_id != user.id:
        friend = UserService.get_user(friend_id, db)
        if not friend:
            raise HTTPException(status_code=404, detail=f"User with id {friend_id} not found")
        
        return { "success": FriendService.delete_friend(user, friend, db) }
    
@router.get(
    path="/v1/friends/common",
    tags={"UserFriends"},
    summary="Get common friends with other user",
    response_model=List[UserBase]
)
async def get_common_friends(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    other_user = UserService.get_user(user_id, db)
    if other_user:
        return FriendService.common_friends(user, other_user, db)
    
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")