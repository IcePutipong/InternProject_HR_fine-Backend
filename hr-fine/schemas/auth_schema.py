from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserRegister(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    emp_id: str
    password: str

class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_tkeon: str
    status: bool
    created_date: datetime.datetime

class ChangePassword(BaseModel):
    current_password: str
    new_password: str