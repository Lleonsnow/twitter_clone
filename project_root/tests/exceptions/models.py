from typing import Tuple


class ModelException(Exception):
    """Базовый класс исключений."""

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        self.message = message

    def __str__(self) -> Tuple[str, int]:
        return self.message, self.status


class TweetNotFound(ModelException):
    """Исключение при отсутствии твита."""

    ...


class TweetNotOwnedByAuthor(ModelException):
    """Исключение при отсутствии связей между твитом и автором."""

    ...


class ErrorMediaType(ModelException):
    ...
