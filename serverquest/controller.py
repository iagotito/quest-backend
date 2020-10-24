from . alchemy import User
from . alchemy import insert_user
from . alchemy import get_user

def create_user(user_data):
    created = insert_user(email=user_data.get('email'), name=user_data.get('name'), password=user_data.get('password'))
    assert created, 'Email already registered.'


def get_user_data(jwt):
    user_email = User.decode_auth_token(jwt)
    
    assert user_email != 'Signature expired.', 'Signature expired.'
    assert user_email != 'Invalid token.', 'Invalid token.'

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
