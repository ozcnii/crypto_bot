import random

import GoodGuard.tokensFabric
import Tools
from GoodGuard.Words import WordsGuard
from GoodGuard.utils import deprecated


def serialize_json_user_token(user_data):
    return {
        "username": user_data.username,
    }


def serialize_json_user_token_restore(user_data):
    return {
        "username": user_data.username,
    }