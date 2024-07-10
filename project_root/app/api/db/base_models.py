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
    """Модель пользователя"""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    address: Mapped[Dict[str, str]] = mapped_column(JSON)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    tweets: Mapped[List["Tweet"]] = relationship(
        "Tweet", back_populates="author", cascade="all, delete-orphan"
    )
    likes: Mapped[List["Like"]] = relationship(
        "Like", back_populates="user", cascade="all, delete-orphan"
    )
    api_key: Mapped["ApiKey"] = relationship(
        "ApiKey", back_populates="user", uselist=False
    )
    followers: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.following_id]",
        back_populates="following",
        viewonly=True,
        cascade="all, delete-orphan",
    )
    following: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.follower_id]",
        back_populates="follower",
        viewonly=True,
        cascade="all, delete-orphan",
    )


class Follower(Base):
    """Модель подписок"""

    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    following_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    follower: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )
    following: Mapped["User"] = relationship(
        "User", foreign_keys=[following_id], back_populates="followers"
    )


class Tweet(Base):
    """Модель твита"""

    __tablename__ = "tweets"

    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    like_count: Mapped[int] = mapped_column(Integer, default=0)
    attachments: Mapped[List["Media"]] = relationship(
        "Media", back_populates="tweet", cascade="all, delete-orphan"
    )
    author: Mapped["User"] = relationship("User", back_populates="tweets")
    likes: Mapped[List["Like"]] = relationship(
        "Like", back_populates="tweet", cascade="all, delete-orphan"
    )


class Media(Base):
    """Модель медиафайла"""

    __tablename__ = "media"

    tweet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tweets.id"), nullable=True
    )
    tweet_data: Mapped[str] = mapped_column(Text, default=None, nullable=True)
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="attachments")


class Like(Base):
    """Модель лайка"""

    __tablename__ = "likes"

    tweet_id: Mapped[int] = mapped_column(Integer, ForeignKey("tweets.id"))
    tweet: Mapped["Tweet"] = relationship("Tweet", back_populates="likes")
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="likes")


class ApiKey(Base):
    """Модель API ключа"""

    __tablename__ = "api_keys"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    user: Mapped["User"] = relationship("User", back_populates="api_key")

    # attachments: Mapped[Dict[str, str | bytes]] = mapped_column(JSON, nullable=True)
    # attachments: Mapped[List[str]] = mapped_column(ARRAY(Text), default=[], nullable=True)
