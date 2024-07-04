from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class Follower(User): ...


class Following(User): ...


class UserProfile(User):
    followers: List[Follower]
    following: List[Following]


class UserResponse(BaseModel):
    result: bool
    user: UserProfile


class Like(BaseModel):
    user_id: int
    name: str


class Tweet(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: User
    likes: List[Like]


class TweetResponse(BaseModel):
    result: bool
    tweet: List[Tweet]
