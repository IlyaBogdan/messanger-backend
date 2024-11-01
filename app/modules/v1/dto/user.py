from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    id: int
    email: EmailStr
    username: str