import re
from typing import List
from pydantic import BaseModel, Field, field_validator, EmailStr
from modules.v1.models.friend_request import FriendRequestStatus

class SetFriendRequestStatus(BaseModel):
    requestId: int = Field(description="Friend request ID", examples=[1, 4, 7, 12])
    status: int = Field(description="Friend request status", examples=[e.value for e in FriendRequestStatus])

class CreateFriendRequest(BaseModel):
    friendId: int = Field(description="Friend user ID", examples=[1, 2, 5])