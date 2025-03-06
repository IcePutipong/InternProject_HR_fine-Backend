from functools import wraps
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db import get_session
import os, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, date, timezone
from typing import Union, Any
from dotenv import load_dotenv

from models import auth_model
from models.auth_model import Users  

load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any], emp_id: str, db: Session, expires_delta: int = None) -> str:
    """
    Creates an access token and includes reset_status from the database.
    """
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    user = db.query(Users).filter(Users.emp_id == emp_id).first()
    if not user:
        raise ValueError("User not found in database")

    reset_status = user.reset_status  


    to_encode = {
        "exp": expires_delta,
        "sub": str(subject),
        "emp_id": emp_id,
        "reset_status": reset_status 
    }

    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encode_jwt

def create_refresh_token(subject: Union[str, Any], emp_id: str, db: Session, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    user = db.query(Users).filter(Users.emp_id == emp_id).first()
    if not user:
        raise ValueError("User not found in database")

    reset_status = user.reset_status

    to_encode = {"exp": expires_delta, "sub": str(subject), "emp_id": emp_id, "reset_status": reset_status}
    encode_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)

    return encode_jwt

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        username = payload['sub']
        data = kwargs['session'].query(auth_model.RefreshToken).filter_by(username=username, access_token=kwargs['dependencies'], status=True).first()
        if data: 
            return func(kwargs['dependencies'], kwargs['session'])
        else:
            return{'msg': "Token Blocked."}
    return wrapper