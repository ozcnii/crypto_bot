from typing import Any


class ManyRequestException(Exception):
    def __init__(self, status_code: int, message: Any):
        self.status_code = status_code
        self.message = message