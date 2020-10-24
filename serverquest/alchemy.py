import datetime

import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from sqlalchemy import Column, String

engine = create_engine('sqlite:///serverquest/database/data.db', echo = True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

SECRET_KEY = 'super-duper-secret-key'


class User(Base):
    __tablename__ = 'user'
    
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
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
        return False
    return True


def get_user(email):
    return User.find_by_email(session, email)
