from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class UserSignupRequest(BaseModel):
  full_name: str = Field(..., min_length=3, examples=["Pankaj hamal"])
  email: EmailStr = Field(..., examples=["pankaj@gmail.com"])
