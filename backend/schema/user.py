from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class UserSignupRequest(BaseModel):
  full_name: str = Field(..., min_length=3, examples=["Pankaj hamal"])
  email: EmailStr = Field(..., examples=["pankaj@gmail.com"])
  password: str = Field(..., min_length=8, max_length=72, examples=["password@123"])

class UserLoginRequest(BaseModel):
  email: EmailStr
  password: str = Field(..., min_length=8, examples=["password@123"]) 


class UserResponse(BaseModel):
  id: int
  username: str
  email: EmailStr

  class Config:
    from_attributes = True
