from . alchemy import User
from . alchemy import insert_user
from . alchemy import get_user
from . alchemy import insert_tag

def create_user(user_data):
    user_repr = insert_user(email=user_data.get('email'), name=user_data.get('name'), password=user_data.get('password'))
    assert user_repr is not None, 'Email already registered.'
    return user_repr


def get_user_data(jwt):
    user_email = User.decode_auth_token(jwt)
    
    assert user_email != 'Signature expired.', 'Signature expired.'
    assert user_email != 'Invalid token.', 'Invalid token.'

    user_repr = get_user(user_email)

    assert user_repr is not None, 'User not found.'

    return user_repr


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
    user_email = User.decode_auth_token(jwt)
    
    assert user_email != 'Signature expired.', 'Signature expired.'
    assert user_email != 'Invalid token.', 'Invalid token.'

    tag_name = tag_data.get('tag_name')
    tag = insert_tag(user_email, tag_name)

    assert tag is not None, f'Tag {tag_name} already exists for the user {user_email}'

    return tag
