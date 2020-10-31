from . alchemy import User
from . alchemy import insert_user
from . alchemy import get_user
from . alchemy import insert_tag
from . alchemy import get_tags
from . alchemy import insert_todo
from . alchemy import get_todos
from . alchemy import todo_mark_as
from . util import get_user_email

def create_user(user_data):
    user_repr = insert_user(email=user_data.get('email'), name=user_data.get('name'), password=user_data.get('password'))
    assert user_repr is not None, 'Email already registered.'
    return user_repr


def get_user_data(jwt):
    user_email = get_user_email(kwt)

    user = get_user(user_email)

    assert user is not None, 'User not found.'

    return user.repr()


def get_jwt(user_data):
    email = user_data.get('email')
    password = user_data.get('password')
    assert email, 'Email is empty.'
    assert password, 'Password is empty.'

    user = get_user(email)

    assert user, 'Email not found.'
    assert password == user.password, 'Wrong password.'

    return user.encode_auth_token(user.email)


def create_tag(jwt, tag_data):
    user_email = get_user_email(jwt)
    tag_name = tag_data.get('tag_name')

    tag = insert_tag(user_email, tag_name)

    assert tag is not None, f'Tag {tag_name} already exists for the user {user_email}'

    return tag


def get_user_tags(jwt):
    user_email = get_user_email(jwt)

    tags = get_tags(user_email)

    return [tag.name for tag in tags]


def create_todo(jwt, tag_name, todo_info):
    assert todo_info.get('description') != '', 'Descriptin is empty.'
    if 'deadline' in todo_info:
        assert todo_info.get('deadline') != '', 'Deadline is provided but is empty.'
    else:
        todo_info['deadline'] = '-'

    user_email = get_user_email(jwt)
    user_tags = get_user_tags(jwt)
    assert tag_name in user_tags, f"User '{user_email}' don't have a tag named '{tag_name}'"

    todo = insert_todo(todo_info.get('description'), todo_info.get('deadline'), tag_name, user_email)

    assert todo is not None, 'Error in todo creation: todo already exists, but the id should be new to each todo.'

    return todo


def get_user_todos(jwt, tag_name, done=None):
    user_email = get_user_email(jwt)
    user_tags = get_user_tags(jwt)
    assert tag_name in user_tags, f"User '{user_email}' don't have a tag named '{tag_name}'"

    todos = get_todos(user_email, tag_name, done)

    return [todo.to_dict() for todo in todos]


def update_todo_done(jwt, tag_name, todo_id, mark_as):
    user_email = get_user_email(jwt)
    user_tags = get_user_tags(jwt)
    assert tag_name in user_tags, f"User '{user_email}' don't have a tag named '{tag_name}'"

    todo = todo_mark_as(todo_id, mark_as)
