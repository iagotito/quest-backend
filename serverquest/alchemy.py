from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from sqlalchemy import Column, String

engine = create_engine('sqlite:///serverquest/database/data.db',echo = True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def repr(self):
        return f'User {self.name}'

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


Base.metadata.create_all(engine)


def insert_user (email, name, password):
    user = User(email=email, name=name, password=password)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        return False
    return True
