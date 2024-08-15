import random

from GoodGuard.Words import bad_words


def ranh(self: int):
    return "".join(random.choices(["🤎", "🤍", "💚", "💛", "💜"], k=self))


def positive_message(negative_message):
    for i in bad_words:
        negative_message = negative_message.replace(i, ranh(len(i)))

    return negative_message


def negative_message_detector(message):
    words = message.split()
    for word in words:
        if word in bad_words:
            return True
    return False