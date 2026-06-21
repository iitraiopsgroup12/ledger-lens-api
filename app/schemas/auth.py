from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    id: str
    name: str


class LoginResponse(BaseModel):
    access_token: str
    user: LoginUser


class UserProfile(BaseModel):
    id: str
    email: EmailStr
    role: str = Field(examples=["analyst", "admin"])
