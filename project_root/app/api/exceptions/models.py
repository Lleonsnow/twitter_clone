from typing import Tuple


class ModelException(Exception):
    def __init__(self, status: int, message: str) -> None:
        self.status = status
        self.message = message

    def __str__(self) -> Tuple[str, int]:
        return self.message, self.status


class TweetNotFound(ModelException):
    ...


class TweetNotOwnedByAuthor(ModelException):
    ...
