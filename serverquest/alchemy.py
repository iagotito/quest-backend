import datetime

import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, String, ForeignKey

engine = create_engine('sqlite:///serverquest/database/data.db', echo = True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

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


Base.metadata.create_all(engine)


def insert_user (email, name, password):
    user = User(email=email, name=name, password=password)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return None
    return user.repr()


def get_user(email):
    return User.find_by_email(session, email)
    

def insert_tag(email, tag_name):
    tag = Tag(name=tag_name, owner=email)
    session.add(tag)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return None
    return tag.repr()


def get_tags(email):
    user = User.find_by_email(session, email)
    tags = user.tags
    return tags
