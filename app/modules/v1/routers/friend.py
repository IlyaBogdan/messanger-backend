from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException

from modules.v1.models.user import User
from modules.v1.dto.user import UserBase
from modules.v1.services import user as UserService
from modules.v1.services import auth as AuthService
from modules.v1.services import friend as FriendService
from modules.v1.dto.friend import SetFriendRequestStatus, CreateFriendRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")
router = APIRouter()    

@router.get(
    path='/v1/friends',
    tags={"UserFriends"},
    summary="Get user friends",
    response_model=List[UserBase]
)
async def friend_list(
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    return user.friends

@router.post(
    path='/v1/friends/friend-request',
    tags={"UserFriends"},
    summary="Create request to add user to friends",
    response_model=dict
)
async def add_to_friends_request(
    data: CreateFriendRequest,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    if data.friendId != user.id:
        friend = UserService.get_user(data.friendId, db)
        if not friend:
            raise HTTPException(status_code=404, detail=f"User with id {data.friendId} not found")
        
        return { "success": FriendService.create_friend_request(data, user, db) }
    
@router.post(
    path='/v1/friends/friends-request/set-status',
    tags={"UserFriends"},
    summary="Set status of friend request",
    response_model=dict
)
async def set_friend_request_status(
    data: SetFriendRequestStatus,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    return { "success": FriendService.set_friend_request_status(data, user, db) }

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