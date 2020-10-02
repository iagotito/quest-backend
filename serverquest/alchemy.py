
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column,Integer, String, ForeignKey

engine = create_engine('sqlite:///serverquest/database/data.db',echo = True)

def setup_bd ():
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        
        email = Column(String, primary_key=True)
        name = Column(String, nullable=False)
        password = Column(String, nullable=False)
        tags = relationship('Tag', backref = 'users')

        def repr(self):
            return f'User {self.name}'

    class Tag(Base):
        __tablename__ = 'tags'

        name = Column(String, primary_key=True)
        owner = Column(String, ForeignKey('users.email'), primary_key=True)
        users = relationship('User')
        todos = relationship('Todo', backref='tags')

        def repr(self):
            return f'Tag {self.name}'

    class Todo(Base):
        __tablename__ = 'todo'

        description = Column(String, primary_key=True)
        finished = Column(Integer, nullable=False)
        tag = Column(String, ForeignKey('tags.name'), nullable=False)
        tags = relationship('Tag')
        
        def rept(self):
            return f'Todo {self.description}'


    Base.metadata.create_all(engine)


