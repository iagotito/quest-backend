import datetime

import jwt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . connect2db import engine

SECRET_KEY = 'super-duper-secret-key'
TOKEN_EXPIRATION_TIME = 60*60*24*30

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    deadline = Column(String)
    done = Column(Integer)
    tag_name = Column(String, ForeignKey('tag.name'))
    owner_email = Column(String, ForeignKey('user.email'))
    tag = relationship('Tag')
    owner = relationship('User')


    def __init__(self, description, deadline, tag_name, owner_email):
        self.description = description
        self.deadline = deadline
        self.done = 0
        self.tag_name = tag_name
        self.owner_email = owner_email


    def repr(self):
        return f'TODO: {self.description}; ID: {self.id}; Deadline: {self.deadline}; Done: {"True" if self.done == 1 else "False"}; Tag: {self.tag_name}; Owner: {self.owner_email};'
 

class Tag(Base):
    __tablename__ = 'tag'
    
    name = Column(String, primary_key=True)
    owner = Column(String, ForeignKey('user.email'), primary_key=True,)
    user = relationship('User')
    todos = relationship(Todo, backref='tags')


    def __init__(self, name, owner):
        self.name = name
        self.owner = owner


    def repr(self):
        return f'Name: {self.name}; Owner: {self.owner};'


class User(Base):
    __tablename__ = 'user'
    
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    tags = relationship(Tag, backref='users')


    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


    def repr(self):
        return f'User {self.name}; Email: {self.email};'

    
    @classmethod
    def find_by_email(cls, session, email):
        return session.query(cls).filter_by(email=email).first()


    def encode_auth_token(self, user_email):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=TOKEN_EXPIRATION_TIME),
                'iat': datetime.datetime.utcnow(),
                'sub': user_email
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            ).decode(encoding=('UTF-8'))
        except Exception as e:
            return e


    @staticmethod
    def decode_auth_token(auth_token):
        auth_token = auth_token.encode(encoding='UTF-8')
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'


Base.metadata.create_all(engine)
