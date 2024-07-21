from collections.abc import Sequence
from typing import List

from api.db.base_models import Media as BaseMedia
from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserSchema(BaseModel):
    """Схема для пользователя."""

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class FollowerSchema(UserSchema):
    """Схема для подписчика."""

    ...


class FollowingSchema(UserSchema):
    """Схема для подписки."""

    ...


class UserWithFollowersSchema(UserSchema):
    """Схема для пользователя с подписками и подписчиками."""

    followers: Sequence[FollowerSchema] = Field(default_factory=list)
    following: Sequence[FollowingSchema] = Field(default_factory=list)


class UserResponseSchema(BaseModel):
    """Схема для ответа на запрос пользователя."""

    result: bool
    user: UserWithFollowersSchema


class LikeSchema(BaseModel):
    """Схема для лайка."""

    user_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class TweetSchema(BaseModel):
    """Схема для твита."""

    id: int
    content: str
    attachments: List[str] = Field(default_factory=list)
    author: UserSchema
    likes: Sequence[LikeSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("attachments", mode="before")
    def convert_attachments(cls, value: List[BaseMedia]) -> List[str]:
        """Преобразование медиафайлов в ссылки."""
        converted = [item.tweet_data for item in value]
        return converted


class BasicResponseSchema(BaseModel):
    """Базовая схема для ответа на запрос."""

    result: bool

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BasicResponseSchema):
    """Схема для обработки ошибки."""

    error_type: str
    error_message: str


class MediaResponseSchema(BasicResponseSchema):
    """Схема для возвращения медиафайла."""

    media_id: int


class TweetsResponseSchema(BasicResponseSchema):
    """Схема для возвращения твитов."""

    tweets: List[TweetSchema] = Field(default_factory=list)


class TweetPostResponseSchema(BasicResponseSchema):
    """Схема для запроса на создание твита."""

    tweet_id: int


class TweetCreateRequest(BaseModel):
    """Схема для создания твита."""

    tweet_data: str
    tweet_media_ids: List[int] | None = []
