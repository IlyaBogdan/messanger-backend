from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    accessToken: str
    refreshToken: str

class RefreshToken(BaseModel):
    refreshToken: str