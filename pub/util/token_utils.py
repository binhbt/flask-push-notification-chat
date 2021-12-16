
import jwt
import datetime
APP_AUTH=""
def encode_auth_token(data_info):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10, seconds=20),
            'iat': datetime.datetime.utcnow(),
            'sub': data_info
        }
        return jwt.encode(
            payload,
            APP_AUTH['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        return e
def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, APP_AUTH['SECRET_KEY'])
        return True, payload['sub']
    except jwt.ExpiredSignatureError:
        return False, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'

def generate_random_token():
    from uuid import uuid4
    rand_token = str(uuid4())
    return rand_token