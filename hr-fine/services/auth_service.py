from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Depends, status
import jwt, os, datetime, string, random, pika, json

from sqlalchemy import desc
from sqlalchemy.orm import Session
from utils.jwt_bearer import JWTBearer
from utils.jwt_util import create_access_token, create_refresh_token, get_hashed_password, verify_password

from database.db import get_session
from models import auth_model
from models.auth_model import RefreshToken, Users
from schemas import auth_schema
from services.email_sending import send_user_registration_email

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

def generate_username(session: Session) -> str:
    """Generate a unique employee ID."""
    current_year = datetime.datetime.now().year
    thai_year = current_year + 543
    base_id = f"{thai_year % 100}"
    
    last_user = (
        session.query(auth_model.Users)
        .filter(auth_model.Users.create_year == thai_year)
        .order_by(desc(auth_model.Users.emp_id))
        .first()
    )

    if last_user and last_user.emp_id.startswith(base_id):
        last_id_number = int(last_user.emp_id[len(base_id):])
        next_id_number = last_id_number + 1
    else:
        next_id_number = 1

    while True:
        emp_id = f"{base_id}{next_id_number:03d}"
        existing_user = session.query(auth_model.Users).filter_by(emp_id=emp_id).first()
        if not existing_user:
            break  
        next_id_number += 1  

    return emp_id

def generate_random_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def register_user(user: auth_schema.UserRegister, session: Session=Depends(get_session)):
    if not user.email:
        raise HTTPException(
            status_code=400,
            detail="Email cannot be Empty.")
    
    existing_email = session.query(auth_model.Users).filter_by(email=user.email).first()
    if existing_email: 
        raise HTTPException(
            status_code=400,
            detail="Email Already Registered.")

    emp_id = generate_username(session)
    existing_emp_id = session.query(auth_model.Users).filter_by(emp_id=emp_id).first()
    if existing_emp_id:
        raise HTTPException(
            status_code=400,
            detail=f"Employee ID {emp_id} already exists.")

    random_password = generate_random_password()
    encyped_password = get_hashed_password(random_password) ### NOTE: don't forget to change to random generated password when register.
    create_year = datetime.datetime.now().year

    new_user = auth_model.Users(
        emp_id = emp_id,
        email = user.email,
        password = encyped_password,
        create_year = create_year,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    send_user_registration_email(to_email=user.email, emp_id=emp_id, password=random_password)
    
    return {
        "email": new_user.email,
        "emp_id": new_user.emp_id,
        "password": random_password
    }


def login_user(request: auth_schema.UserLogin, db: Session=Depends(get_session)):
    user = db.query(Users).filter(Users.emp_id == request.emp_id).first()
    
    if not request.emp_id or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and Password cannot be Empty."
        )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Username does not Exist."
        )
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password."
        )
    
    access = create_access_token(user.id, emp_id=user.emp_id)
    refresh = create_refresh_token(user.id, emp_id=user.emp_id)

    token_db = auth_model.RefreshToken(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)

    return {
        "access_token": access,
        "refresh_token": refresh
    }

def logout_user(dependencies=Depends(JWTBearer()), db:Session=Depends(get_session)):
    token = dependencies
    try: 
        payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has Expired."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token."
        )
    
    user_id = payload['sub']
    token_record = (db.query(RefreshToken)
                    .filter(
                        RefreshToken.user_id == user_id,
                        RefreshToken.access_token == token,
                    ).first())

    if token_record:
        token_record.status = False
        db.add(token_record)
        db.commit()
        db.refresh(token_record)

    return {"message": "LogOut Successfully."}


def change_password(emp_id: str, request: auth_schema.ChangePassword, db: Session = Depends(get_session)):
    user = db.query(auth_model.Users).filter(Users.emp_id == emp_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found.")
    
    if not verify_password(request.current_password, user.password):
        raise HTTPException(status_code=400, detail="Current Password is incorrect.")
    
    hashed_new_password = get_hashed_password(request.new_password)
    user.password = hashed_new_password
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Password changed Successfully."}

def change_temporary_password(emp_id: str, new_password: str, session: Session = Depends(get_session)):
    user = session.query(auth_model.Users).filter(Users.emp_id == emp_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not Found.")
    
    if user.reset_status is True:
        raise HTTPException(status_code=403, detail="User already change temporary Password.")
    
    hash_password = get_hashed_password(new_password)
    user.password = hash_password
    user.reset_status = True
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "Password reset successfully"}


def access_refresh_token(refresh_token: str, db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh Token has Expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Refresh Token.")
    
    user_id = payload["sub"]
    token_record = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.refresh_token == refresh_token,
            RefreshToken.status == True,
        ).first()
    ) 
    if not token_record:
        raise HTTPException(status_code=401, detail= "Refresh Token is Invalid or Revoked.")
    
    new_access_token = create_access_token(user_id)
    token_record.access_token = new_access_token
    db.add(token_record)
    db.commit
    db.refresh(token_record)



