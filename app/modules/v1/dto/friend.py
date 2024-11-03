from pydantic import BaseModel, Field, field_validator
from modules.v1.models.friend_request import FriendRequestStatus

class SetFriendRequestStatus(BaseModel):
    requestId: int = Field(description="Friend request ID", examples=[1, 4, 7, 12])
    status: int = Field(description="Friend request status", examples=[e.value for e in FriendRequestStatus])
    
    @field_validator('status')
    def check_given_status(cls, value):
        """Check valid status"""
        if value not in [e.value for e in FriendRequestStatus]:
            raise ValueError(f"Status must be one of {[e.value for e in FriendRequestStatus]}")
        return value

class CreateFriendRequest(BaseModel):
    friendId: int = Field(description="Friend user ID", examples=[1, 2, 5])
