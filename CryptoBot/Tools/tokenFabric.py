import jwt
import datetime


def generate_jwt_token(user_id):
    """
    Метод генерации токена пользователя (для обращения к API)
    :param user_id: Передайте user id пользователя из Telegram
    :return: Возвращает строку, т.е токен. Токен должен обновляться каждую итерацию команды /start
    """
    token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, 'MY_SECRET_KEY')
    return token