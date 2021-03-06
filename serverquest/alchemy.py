from sqlalchemy.exc import IntegrityError

from . connect2db import session
from . models import User, Tag, Todo


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
    user = User.find_by_email(session, email)
    assert user is not None, f'User {email} not found.'

    return user
    

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
    user = get_user(email)
    tags = user.tags
    return tags


def get_tag(tag_name, email):
    return session.query(Tag).filter_by(name=tag_name, owner=email).first() 


def insert_todo(description, deadline, tag_name, email):
    todo = Todo(description=description, deadline=deadline, tag_name=tag_name, owner_email=email)
    session.add(todo)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return None
    return todo.repr()


def get_todos(email, tag_name, done=None):
    tag = get_tag(tag_name, email)

    assert tag is not None, f"User {email} don't have tag {tag_name}."

    if done is not None:
        return session.query(Todo).filter_by(owner_email=email, tag_name=tag_name, done=int(done)).all()

    return tag.todos

def get_todo(todo_id):
    todo = session.query(Todo).filter_by(id=todo_id).first()
    assert todo, f'Todo {todo_id} not found.'
    return todo


def todo_mark_as(todo_id, mark_as):
    todo = get_todo(todo_id)

    todo.done = mark_as

    session.commit()

    return todo.repr()
