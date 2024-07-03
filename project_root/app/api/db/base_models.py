from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Integer, ForeignKey, JSON, Sequence, ARRAY, Text


class Base(DeclarativeBase, AsyncAttrs):
    id: Mapped[int] = mapped_column(Integer, Sequence(f"{__name__}_id_seq"), primary_key=True)


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    address: Mapped[Dict[str, str]] = mapped_column(JSON)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    twits: Mapped[List["Twit"]] = relationship("Twit", back_populates="user")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="user")
    followers: Mapped[List["Follower"]] = relationship("Follower", back_populates="user")


class Twit(Base):
    __tablename__ = "twits"

    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    attachments: Mapped[Dict[str, str]] = mapped_column(JSON, nullable=True)
    # attachments: Mapped[List[str]] = mapped_column(ARRAY(Text), default=[], nullable=True)
    media: Mapped[List["Media"]] = relationship("Media", back_populates="twit")
    user: Mapped["User"] = relationship("User", back_populates="twits")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="twit")


class Media(Base):
    __tablename__ = "media"

    twit_id: Mapped[int] = mapped_column(Integer, ForeignKey("twits.id"))
    twit_data: Mapped[str] = mapped_column(String(200), default=None, nullable=True)
    twit: Mapped["Twit"] = relationship("Twit", back_populates="media")


class Like(Base):
    __tablename__ = "likes"

    twit_id: Mapped[int] = mapped_column(Integer, ForeignKey("twits.id"))
    twit: Mapped["Twit"] = relationship("Twit", back_populates="likes")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="likes")


class Follower(Base):
    __tablename__ = "followers"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="followers")
