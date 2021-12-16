from util.token_utils import generate_random_token
from util.redis_utils import save_value_key, get_value_key
def session_token_generate(data):
    token =generate_random_token()
    save_value_key(token, "ok", 60)
    return token
def validate_session_token(token):
    data = get_value_key(token)
    print(data)
    if data:
        return True
    return False