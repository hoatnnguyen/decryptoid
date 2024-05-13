from fastapi import Request, HTTPException
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import schemas
from passlib.context import CryptContext
from . import crud
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

class RequiredLogin(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(RequiredLogin, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        headers: HTTPAuthorizationCredentials = await super(RequiredLogin, self).__call__(request)
        if headers:
            if not headers.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            token = headers.credentials

            payload = self.verify_jwt(token)

            if payload is None:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")

            return payload.get("sub")
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str):
        try:
            payload = jwt.decode(token=jwt_token, key=SECRET_KEY,
                                 algorithms=ALGORITHM)
        except Exception as e:
            print(e)
            payload = None

        return payload
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Set expiration to 1 month
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_user(db: Session, user: schemas.UserCreate):
    plaintext = user.password
    user_db = crud.get_user_by_username(db=db, username=user.username)
    # If user is not found or passwords are unmatched, return False
    if user_db is None:
        return False
    if not pwd_context.verify(secret=plaintext, hash=user_db.hashed_password):
        return False
    return True

def get_current_user_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.JWTError:
        raise ValueError("Invalid token. Please provide a valid JWT token.")
