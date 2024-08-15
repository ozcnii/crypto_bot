import jwt

import base64
import hashlib
import secrets


import re
import string
import random


from GoodGuard.utils import deprecated
from GoodGuard import client_id, SECRET_KEY


def create_hash(context: str) -> str:
    hash_object = hashlib.sha256(context.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def get_hash(context: str, context_2: str) -> bool:
    return create_hash(context) == create_hash(context_2)


def generate_access_token(user_data: dict) -> str:
    if user_data is not None:
        password_token = user_data['username']

        token_id = secrets.token_hex()
        user_data['token_id'] = token_id
        user_data['username'] = create_hash(password_token)

        access_token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')
        return access_token


def decode_access_token(access_token: str) -> dict:
    try:
        decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        token_id = decoded_token.pop('token_id')
        return decoded_token
    except jwt.ExpiredSignatureError:
        return 'Access token expired'
    except jwt.InvalidTokenError:
        return "Invalid token"


def generate_verification_code(length: int) -> str:
    characters = string.ascii_letters + string.digits
    one_time_code = ''.join(random.choice(characters) for _ in range(length))
    return one_time_code


def check_client_id(client_id_request):
    if str(client_id_request) in client_id:
        return True
    else:
        return False


def check_email_user(email_request):
    EMAIL_PATTERN = re.compile("^(?=.{1,64}@)[A-Za-z0-9_-]+(\\.[A-Za-z0-9_-]+)*@" \
                               + "[^-][A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)*(\\.[A-Za-z]{2,})$")
    if not EMAIL_PATTERN.match(email_request):
        return False

    return True