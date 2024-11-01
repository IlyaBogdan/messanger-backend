import re
from pydantic import BaseModel, Field, field_validator

class AuthRequest(BaseModel):
    email: str
    password: str = Field(min_length=6, )

    @field_validator('password')
    def value_must_match_regex(cls, password):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(regex, password):
            raise ValueError('Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character')

        return password

class AuthResponse(BaseModel):
    accessToken: str
    refreshToken: str

class RefreshToken(BaseModel):
    refreshToken: str