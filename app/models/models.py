from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    email = Column(String(64), unique=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))

    resumes = relationship('Resume', back_populates='owner')
    batches = relationship('Batch', back_populates='user')
    jobs = relationship('Jobs', back_populates='owner')
    tag = relationship('ResumeTag', back_populates='user')

    @hybrid_property
    def resume_count(self):
        return len(self.resumes)


class Resume(Base):
    __tablename__ = 'resume'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    object_id = Column(String(24), index=True, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow())
    filename = Column(String(255))
    batch_id = Column(String(24), ForeignKey('batch.id'))
    content = Column(JSON)
    tag_id = Column(Integer, ForeignKey('resumetag.id'))

    owner = relationship('User', back_populates='resumes')
    batch = relationship('Batch', back_populates='resumes')
    tag = relationship('ResumeTag', back_populates='resumes')


class Batch(Base):
    __tablename__ = 'batch'

    id = Column(String(24), primary_key=True, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow())
    resumes = relationship('Resume', back_populates='batch')
    user = relationship('User', back_populates='batches')

    @hybrid_property
    def item_count(self):
        return len(self.resumes)


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(256))
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow())

    owner = relationship('User', back_populates='jobs')


class ResumeTag(Base):
    __tablename__ = 'resumetag'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(256), index=True)
    description = Column(Text)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow())

    user = relationship('User', back_populates='tag')
    resumes = relationship('Resume', back_populates='tag')

    @hybrid_property
    def resume_count(self):
        return len(self.resumes)

    @hybrid_property
    def disk_size(self):
        return 1e6
