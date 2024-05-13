from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    password: str

class UserLogin(UserBase):
    password: str

class UserLoginResponse(UserBase):
    accessToken: str

    class Config:
        from_attributes = True

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class CipherActivityResponse(BaseModel):
    input_content: str
    cipher_algorithm: str
    cipher_mode: str
    timestamp: datetime

    class Config:
        from_attributes = True

class CipherActivityCreate(BaseModel):
    # input_content: str
    # cipher_algorithm: str
    # cipher_mode: str
    # accessToken: str
    input_content: str
    cipher_algorithm: str
    cipher_mode: str
    timestamp: datetime = datetime.now()
    user_id: int

    class Config:
        from_attributes = True
