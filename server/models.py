from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    cipher_activities = relationship("CipherActivity", back_populates="user")

class CipherActivity(Base):
    __tablename__ = "cipher_activities"

    id = Column(Integer, primary_key=True)
    input_content = Column(Text)
    cipher_algorithm = Column(String)
    cipher_mode = Column(String)
    key = Column(String)
    timestamp = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="cipher_activities")

# class SimpleSubstitution(Base):
#     __tablename__ = "simple_substitutions"

#     id = Column(Integer, primary_key=True)
#     input_text = Column(Text)
#     cipher_mode = Column(String)
#     timestamp = Column(DateTime, default=datetime.now())
#     user_id = Column(Integer, ForeignKey("users.id"))

#     user = relationship("User", back_populates="simple_substitution")

# class DoubleTransposition(Base):
#     __tablename__ = "double_transpositions"

