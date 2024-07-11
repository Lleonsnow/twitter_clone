import base64
from collections.abc import Sequence
from typing import Dict, List

from pydantic import BaseModel, Field, model_validator

from app.api.db.base_models import Media as BaseMedia


class UserSchema(BaseModel):
    """Схема для пользователя"""

    id: int
    name: str

    class Config:
        from_attributes = True


class FollowerSchema(UserSchema):
    """Схема для подписчика"""

    ...


class FollowingSchema(UserSchema):
    """Схема для подписки"""

    ...


class UserWithFollowersSchema(UserSchema):
    """Схема для пользователя с подписками и подписчиками"""

    followers: Sequence[FollowerSchema] = Field(default_factory=list)
    following: Sequence[FollowingSchema] = Field(default_factory=list)


class UserResponseSchema(BaseModel):
    """Схема для ответа на запрос пользователя"""

    result: bool
    user: UserWithFollowersSchema


class MediaSchema(BaseModel):
    """Схема для медиафайла"""

    tweet_data: str

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def decode_tweet_data(cls, media: BaseMedia | Dict) -> Dict:
        """Декодирует tweet_data в str"""
        data = (
            media.tweet_data
            if isinstance(media, BaseMedia)
            else media["tweet_data"]
        )
        uid = (
            media.tweet_id
            if isinstance(media, BaseMedia)
            else media["tweet_id"]
        )

        return {
            "tweet_id": uid,
            "tweet_data": (
                base64.b64encode(data).decode("utf-8")
                if type(data) is bytes
                else data
            ),
        }


class LikeSchema(BaseModel):
    """Схема для лайка"""

    user_id: int
    name: str

    class Config:
        from_attributes = True


class TweetSchema(BaseModel):
    """Схема для твита"""

    id: int
    content: str
    attachments: Sequence[MediaSchema] = Field(default_factory=list)
    author: UserSchema
    likes: Sequence[LikeSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class BasicResponseSchema(BaseModel):
    """Базовая схема для ответа на запрос"""

    result: bool

    class Config:
        from_attributes = True


class ErrorResponse(BasicResponseSchema):
    """Схема для обработки ошибки"""

    error_type: str
    error_message: str


class MediaResponseSchema(BasicResponseSchema):
    """Схема для возвращения медиафайла"""

    media_id: int


class TweetsResponseSchema(BasicResponseSchema):
    """Схема для возвращения твитов"""

    tweets: List[TweetSchema] = Field(default_factory=list)


class TweetPostResponseSchema(BasicResponseSchema):
    """Схема для запроса на создание твита"""

    tweet_id: int


class TweetCreateRequest(BaseModel):
    """Схема для создания твита"""

    tweet_data: str
    tweet_media_ids: List[int] | None = []
