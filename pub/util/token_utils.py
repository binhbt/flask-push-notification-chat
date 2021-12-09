
import jwt
import datetime
from config import APP_AUTH

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
# @staticmethod
def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, APP_AUTH['SECRET_KEY'])
        # if not PUBLIC_KEY in payload['sub']:
        #     return False, 'Invalid token. Please log in again.'

        # is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        # if is_blacklisted_token:
        #     return False, 'Token blacklisted. Please log in again.'
        # else:
        return True, payload['sub']
    except jwt.ExpiredSignatureError:
        return False, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'
