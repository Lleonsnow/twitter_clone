from typing import Sequence
from pydantic import BaseModel, ConfigDict, Field


class BasicResponse(BaseModel):
    result: bool
    status_code: int | None = None


class MediaResponse(BasicResponse):
    media_id: int


class ErrorResponse(BasicResponse):
    """Схема для обработки ошибки"""

    error_type: str
    error_message: str


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AddressSchema(BaseSchema):
    street: str
    city: str


class ApiKeySchema(BaseSchema):
    name: str


class MediaSchema(BaseSchema):
    tweet_data: str


class LikeSchema(BaseSchema):
    name: str


class SimplifiedUserSchema(BaseSchema):
    name: str
    address: AddressSchema
    phone: str
    email: str
    api_key: ApiKeySchema


class TweetSchema(BaseSchema):
    content: str
    author: SimplifiedUserSchema
    attachments: Sequence[MediaSchema]
    likes: Sequence[LikeSchema] = Field(default_factory=list)
    like_count: int


class FollowerSchema(BaseSchema):
    follower: SimplifiedUserSchema
    following: SimplifiedUserSchema


class UserSchema(BaseSchema):
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
