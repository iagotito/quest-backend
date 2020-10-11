from . alchemy import insert_user

def create_user (user_data):
    created = insert_user(email=user_data.get('email'), name=user_data.get('name'), password=user_data.get('password'))
    assert created, 'Email already registered.'
