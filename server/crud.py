from datetime import datetime
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username, 
        hashed_password=hashed_pw,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_cipher_activity(db: Session, input_content, cipher_algorithm, cipher_mode, key, user_id):
    db_cipher_acitivity = models.CipherActivity(
        input_content=input_content,
        cipher_algorithm = cipher_algorithm,
        cipher_mode = cipher_mode,
        key=key,
        timestamp=datetime.now(),
        user_id=user_id
    )
    db.add(db_cipher_acitivity)
    db.commit()
    db.refresh(db_cipher_acitivity)
    return db_cipher_acitivity
