from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    email = Column(String(64), unique=True, index=True)
    username = Column(String(64), unique=True, index=True)

    password_hash = Column(String(128))

    token = Column(String(32), unique=True, index=True)
    token_expiration = Column(DateTime)

    resumes = relationship('ResumeIndex', back_populates='owner')

class ResumeIndex(Base):
    __tablename__ = 'resumeindex'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    object_id = Column(String(24), index=True, unique=True)  # mongodb object_id
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow())
    filename = Column(String(255))
    batch_id = Column(String(25))  # 'b' + oid

    owner = relationship('User', back_populates='resumes')
