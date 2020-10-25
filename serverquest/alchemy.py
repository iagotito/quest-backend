from sqlalchemy.exc import IntegrityError

from . connect2db import session
from . models import User, Tag


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
