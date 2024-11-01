from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException

from modules.v1.models.user import User
from modules.v1.dto.chat import ChatBase
from modules.v1.services import auth as AuthService
from modules.v1.services import chat as ChatService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")
router = APIRouter()

@router.post(
    path='/v1/chat',
    tags={"Messanger"},
    summary="Create new chat",
    response_model=ChatBase
)
async def create_new_chat(
    data: ChatBase,
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    chat = ChatService.create_new_chat(data, db)
    if chat:
        return chat
    

@router.get(
    path='/v1/chat/{id}',
    tags={"Messanger"},
    summary="Get chat info by ID",
    response_model=ChatBase
)
async def get_user_chat(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    chat = ChatService.get_user_chat(id, user, db)
    if chat:
        return chat
    
    raise HTTPException(status_code=404, detail=f"User have no chat with id {id}")

@router.delete(
    path='/v1/chat/{id}',
    tags={"Messanger"},
    summary="Remove user chat by ID",
    description="Soft removal is used",
    response_model=ChatBase
)
async def delete_user_chat(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    chat = ChatService.get_user_chat(id, user, db)
    if chat:
        return ChatService.remove_user_chat(id, db)

    raise HTTPException(status_code=404, detail=f"User have no chat with id {id}")

@router.put(
    path='/v1/chat/{id}',
    tags={"Messanger"},
    summary="Update user chat by ID",
    response_model=ChatBase
)
async def update_user_chat(
    data: ChatBase,
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    chat = ChatService.get_user_chat(data.id, user, db)
    if chat:
        return ChatService.update_user_chat(data, db)

    raise HTTPException(status_code=404, detail=f"User have no chat with id {data.id}")

@router.get(
    path='/v1/chat/get-all',
    tags={"Messanger"},
    summary="Get user chats",
    response_model=List[ChatBase]
)
async def user_chats(
    db: Session = Depends(get_db),
    user: User = Depends(AuthService.get_current_user),
    token: str = Depends(oauth2_scheme)
):
    return user.chats