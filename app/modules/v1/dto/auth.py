import re
from pydantic import BaseModel, Field, field_validator, EmailStr

class AuthRequest(BaseModel):
    email: EmailStr = Field(description="User's email", examples=["someemail@email.com"])
    password: str = Field(description="User's password", examples=["Secutity&123"])

    @field_validator('password')
    def value_must_match_regex(cls, password):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(regex, password):
            raise ValueError('Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character')

        return password
    
class LoginDto(BaseModel):
    email: EmailStr = Field(description="User's email", examples=["someemail@email.com"])
    password: str = Field(description="User's password", examples=["Secutity&123"])

class AuthResponse(BaseModel):
    accessToken: str = Field(description="Access token", examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.DQ2MTgyNX0.4mB2SICM3gK59bByG7S3EGrvkTunk0u5zBRkj-flswA"])
    refreshToken: str = Field(description="Refresh token", examples=["eyJhbGciOiJJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lZW1haWwxQGdtYWlsLmNvbSIsImV4cCIaeTc1A"])

class RefreshToken(BaseModel):
    refreshToken: str = Field(description="Refresh token", examples=["eyJhbGciOiJJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzb21lZW1haWwxQGdtYWlsLmNvbSIsImV4cCIaeTc1A"])

class ResetPasswordInit(BaseModel):
    email: EmailStr = Field(description="User's email", examples=["someemail@email.com"])
    
class ChangePassword(BaseModel):
    newPassword: str = Field(description="User's password", examples=["Secutity&123"])
    resetToken: str

    @field_validator('newPassword')
    def value_must_match_regex(cls, newPassword):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(regex, newPassword):
            raise ValueError('Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character')

        return newPassword