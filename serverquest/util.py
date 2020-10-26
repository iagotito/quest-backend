from . models import User


def get_user_email(jwt):
    user_email = User.decode_auth_token(jwt)
    
    assert user_email != 'Signature expired.', 'Signature expired.'
    assert user_email != 'Invalid token.', 'Invalid token.'

    return user_email
