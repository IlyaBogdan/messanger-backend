from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from modules.v1.dto.user import UserBase, AddFriend
from modules.v1.services import user as UserService

router = APIRouter()    

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
async def update(data: UserBase, db: Session = Depends(get_db)):
    user = UserService.update(data, db)
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

@router.get(
    path='/v1/user/friends/get-all',
    tags={"User"},
    summary="Get user friends",
    response_model=List[UserBase]
)
async def friends(db: Session = Depends(get_db)):
    id_ = 7
    user = UserService.get_user(id_, db)
    if user:
        return user.friends
    
    raise HTTPException(status_code=404, detail=f"User with id {id_} not found")

@router.post(
    path='/v1/user/friends/add-friend',
    tags={"User"},
    summary="Add user to friends",
    response_model=dict
)
async def add_to_friends(data: AddFriend, db: Session = Depends(get_db)):
    id_ = 7
    user = UserService.get_user(id_, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id_} not found")
    
    friend = UserService.get_user(data.friend_id, db)
    if not friend:
        raise HTTPException(status_code=404, detail=f"User with id {data.friend_id} not found")
    
    UserService.add_to_friends(user, friend, db)
    return { "success": True }

@router.delete(
    path='/v1/user/friends/delete-friend',
    tags={"User"},
    summary="Delete user from friend list",
    response_model=dict
)
async def delete_friend(data: AddFriend, db: Session = Depends(get_db)):
    id_ = 7
    user = UserService.get_user(id_, db)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id_} not found")
    
    friend = UserService.get_user(data.friend_id, db)
    if not friend:
        raise HTTPException(status_code=404, detail=f"User with id {data.friend_id} not found")
    
    UserService.delete_friend(user, friend, db)
    return { "success": True }