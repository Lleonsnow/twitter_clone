from typing import Dict, List

from sqlalchemy import (
    ARRAY,
    JSON,
    ForeignKey,
    Integer,
    Sequence,
    String,
    Text,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase, AsyncAttrs):
    id: Mapped[int] = mapped_column(
        Integer, Sequence(f"{__name__}_id_seq"), primary_key=True
    )


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    address: Mapped[Dict[str, str]] = mapped_column(JSON)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    tweets: Mapped[List["Tweet"]] = relationship("Tweet", back_populates="user")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="user")
    api_key: Mapped["ApiKey"] = relationship(
        "ApiKey", back_populates="user", uselist=False
    )
    followers: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.following_id]",
        back_populates="following",
        viewonly=True,
    )
    following: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.follower_id]",
        back_populates="follower",
        viewonly=True,
    )


class Follower(Base):
    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    following_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )

    follower: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )
    following: Mapped["User"] = relationship(
        "User", foreign_keys=[following_id], back_populates="followers"
    )


class Tweet(Base):
    __tablename__ = "tweets"

    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    attachments: Mapped[Dict[str, str]] = mapped_column(JSON, nullable=True)
    # attachments: Mapped[List[str]] = mapped_column(ARRAY(Text), default=[], nullable=True)
    like_count: Mapped[int] = mapped_column(Integer, default=0)
    media: Mapped[List["Media"]] = relationship("Media", back_populates="tweet")
    user: Mapped["User"] = relationship("User", back_populates="tweets")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="tweet")


class Media(Base):
    __tablename__ = "media"

    tweet_id: Mapped[int] = mapped_column(Integer, ForeignKey("tweets.id"))
    tweet_data: Mapped[str] = mapped_column(String(200), default=None, nullable=True)
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="media")


class Like(Base):
    __tablename__ = "likes"

    tweet_id: Mapped[int] = mapped_column(Integer, ForeignKey("tweets.id"))
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="likes")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="likes")


class ApiKey(Base):
    __tablename__ = "api_keys"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    user: Mapped["User"] = relationship("User", back_populates="api_key")
