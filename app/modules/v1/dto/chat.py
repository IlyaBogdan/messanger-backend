import re
from typing import List
from pydantic import BaseModel, Field, field_validator, EmailStr

class ChatBase(BaseModel):
    id: int = Field(description="Chat ID", examples=[1, 2, 5])
    title: str = Field(description="Chat title", examples=["Some title"])
    users: List[int] = Field(description="List of users in chat", examples=[[1, 2], [1, 2, 3]])