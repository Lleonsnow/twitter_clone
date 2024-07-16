from typing import Sequence
from pydantic import BaseModel, ConfigDict, UUID4, Field


class BaseSchema(BaseModel):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)


class AddressSchema(BaseSchema):
    street: str
    city: str


class ApiKeySchema(BaseSchema):
    name: str


class MediaSchema(BaseSchema):
    tweet_data: str


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
    tweets: Sequence[TweetSchema] = Field(default_factory=list)
    followers: Sequence[FollowerSchema] = Field(default_factory=list)
    following: Sequence[FollowerSchema] = Field(default_factory=list)
