from typing import List
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class Follower(User):
    ...


class Following(User):
    ...


class UserProfile(User):
    followers: List[Follower]
    following: List[Following]


class UserResponse(BaseModel):
    result: bool
    user: UserProfile
