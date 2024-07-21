from typing import Sequence

from pydantic import BaseModel, ConfigDict, Field


class BasicResponse(BaseModel):
    """Базовая схема для ответа на запрос."""

    result: bool
    status_code: int | None = None


class MediaResponse(BasicResponse):
    """Схема для возвращения медиафайла."""

    media_id: int


class ErrorResponse(BasicResponse):
    """Схема для обработки ошибки."""

    error_type: str
    error_message: str


class BaseSchema(BaseModel):
    """Базовая схема для модели."""

    model_config = ConfigDict(from_attributes=True)


class AddressSchema(BaseSchema):
    """Схема для адреса."""

    street: str
    city: str


class ApiKeySchema(BaseSchema):
    """Схема для API ключа."""

    name: str


class MediaSchema(BaseSchema):
    """Схема для медиафайла."""

    tweet_data: str
    media_id: int | None = None


class LikeSchema(BaseSchema):
    """Схема для лайка."""

    name: str


class SimplifiedUserSchema(BaseSchema):
    """Схема для упрощенного пользователя."""

    name: str
    address: AddressSchema
    phone: str
    email: str
    api_key: ApiKeySchema


class TweetSchema(BaseSchema):
    """Схема для твита."""

    content: str
    author: SimplifiedUserSchema
    attachments: Sequence[MediaSchema]
    likes: Sequence[LikeSchema] = Field(default_factory=list)
    like_count: int


class FollowerSchema(BaseSchema):
    """Схема для подписчика."""

    follower: SimplifiedUserSchema
    following: SimplifiedUserSchema


class UserSchema(BaseSchema):
    """Схема для пользователя."""

    name: str
    username: str
    email: str
    address: AddressSchema
    phone: str
    api_key: ApiKeySchema
    likes: Sequence[LikeSchema] = Field(default_factory=list)
    tweets: Sequence[TweetSchema] = Field(default_factory=list)
    followers: Sequence[FollowerSchema] = Field(default_factory=list)
    following: Sequence[FollowerSchema] = Field(default_factory=list)
