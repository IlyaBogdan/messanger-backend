from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str]