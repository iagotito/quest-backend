from . alchemy import insert_user
from . alchemy import get_user

def create_user(user_data):
    created = insert_user(email=user_data.get('email'), name=user_data.get('name'), password=user_data.get('password'))
    assert created, 'Email already registered.'


def get_jwt(user_data):
    email = user_data.get('email')
    password = user_data.get('password')

    user = get_user(email)

    assert password == user.password, 'Wrong password.'

    return user.encode_auth_token(user.email)
