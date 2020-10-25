import datetime

import jwt
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . connect2db import Base

SECRET_KEY = 'super-duper-secret-key'
TOKEN_EXPIRATION_TIME = 60*60*24*30


class Tag(Base):
    __tablename__ = 'tag'
    
    name = Column(String, primary_key=True)
    owner = Column(String, ForeignKey('user.email'), primary_key=True,)
    user = relationship('User')


    def repr(self):
        return f'Name: {self.name}; Owner: {self.owner};'


class User(Base):
    __tablename__ = 'user'
    
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    tags = relationship(Tag, backref='users')


    def repr(self):
        return f'User {self.name}; Email: {self.email};'


    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    
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
