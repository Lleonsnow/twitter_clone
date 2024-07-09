import base64
from collections.abc import Sequence
from typing import List, Dict
from pydantic import BaseModel, Field, model_validator

from app.api.db.base_models import Media as BaseMedia


class UserSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class FollowerSchema(UserSchema): ...


class FollowingSchema(UserSchema): ...


class UserProfileSchema(UserSchema):
    followers: Sequence[FollowerSchema] = Field(default_factory=list)
    following: Sequence[FollowingSchema] = Field(default_factory=list)


class UserResponseSchema(BaseModel):
    result: bool
    user: UserProfileSchema


class MediaSchema(BaseModel):
    # tweet_id: int
    tweet_data: str

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def decode_tweet_data(cls, media: BaseMedia | Dict) -> Dict:
        data = media.tweet_data if isinstance(media, BaseMedia) else media["tweet_data"]
        uid = media.tweet_id if isinstance(media, BaseMedia) else media["tweet_id"]

        return {"tweet_id": uid, "tweet_data": base64.b64encode(data).decode("utf-8") if type(data) is bytes else data}


class LikeSchema(BaseModel):
    user_id: int
    name: str

    class Config:
        from_attributes = True


class TweetSchema(BaseModel):
    id: int
    content: str
    attachments: Sequence[MediaSchema] = Field(default_factory=list)
    author: UserSchema
    likes: Sequence[LikeSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ResponseSchema(BaseModel):
    result: bool

    class Config:
        from_attributes = True


class ErrorResponse(ResponseSchema):
    error_type: str
    error_message: str


class MediaResponseSchema(ResponseSchema):
    media_id: int


class TweetResponseSchema(ResponseSchema):
    tweets: List[TweetSchema] = Field(default_factory=list)


class TweetResponsePostSchema(ResponseSchema):
    tweet_id: int


class TweetCreateRequest(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int] | None = []
