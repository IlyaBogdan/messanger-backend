from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    id: int = Field(description="User ID", examples=[1, 2, 5])
    email: EmailStr = Field(description="User's email", examples=["someemail@email.com"])
    username: Optional[str] = Field(description="Username", examples=["Bill Joe", "Pedro Pascal"])

