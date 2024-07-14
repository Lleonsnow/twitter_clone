import random
from collections.abc import Sequence
from http import HTTPStatus
from typing import List

from sqlalchemy import case, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from app.api.core.pydantic_models import (
    ErrorResponse,
    TweetCreateRequest,
    TweetSchema,
)
from app.api.db.base_models import Follower as BaseFollower
from app.api.db.base_models import Like as BaseLike
from app.api.db.base_models import Media as BaseMedia
from app.api.db.base_models import Tweet as BaseTweet
from app.api.db.base_models import User as BaseUser
from app.api.exceptions.error_handler import error_handler
from app.api.exceptions.models import TweetNotFound, TweetNotOwnedByAuthor
from app.api.services.like import delete_like_by_tweet_id_and_user_id
from app.api.services.media import get_medias_from_base


async def create_tweets_flush(
    tweets: List[BaseTweet], session: AsyncSession
) -> List[BaseTweet]:
    """Инициализация тестовых твитов в базе данных"""
    for tweet in tweets:
        session.add(tweet)
    await session.flush()
    return tweets


async def save_user_tweets_with_likes_and_media(
    tweets: List[BaseTweet],
    user: BaseUser,
    medias: List[str],
    session: AsyncSession,
) -> None:
    """Инициализация тестовых твитов в базе данных"""
    for tweet in tweets:
        random_like = random.randint(0, 1)
        tweet.author = user
        media_file = medias.pop()

        media = BaseMedia(tweet=tweet, tweet_data=media_file)

        if random_like:
            like = BaseLike(tweet=tweet, user=user, name=user.name)
            tweet.like_count = 1
            session.add(like)

        session.add(media)


async def get_all_tweets(
    user: BaseUser, session: AsyncSession
) -> Sequence[BaseTweet]:
    """Получение всех твитов с сортировкой по подписчикам
    и количеством лайков по твитам"""
    follower_alias = aliased(BaseFollower)
    user_alias = aliased(BaseUser)

    query = (
        select(BaseTweet)
        .join(
            follower_alias,
            follower_alias.following_id == BaseTweet.user_id,
            isouter=True,
        )
        .join(
            user_alias,
            user_alias.id == follower_alias.following_id,
            isouter=True,
        )
        .options(selectinload(BaseTweet.attachments))
        .options(selectinload(BaseTweet.author))
        .options(selectinload(BaseTweet.likes).selectinload(BaseLike.user))
        .order_by(
            case(
                (follower_alias.follower_id == user.id, True), else_=False
            ).desc(),
            BaseTweet.like_count.desc(),
        )
    )

    result = await session.execute(query)
    return result.scalars().all()


async def tweets_as_schema(
    tweets: Sequence[BaseTweet],
) -> List[TweetSchema]:
    """Преобразование твитов в схему"""
    tweet_schemas = [TweetSchema.model_validate(tweet) for tweet in tweets]
    return tweet_schemas


async def create_new_tweet(
    request: TweetCreateRequest, user: BaseUser, session: AsyncSession
) -> BaseTweet:
    """Создание нового твита"""
    medias = await get_medias_from_base(request.tweet_media_ids, session)
    tweet = BaseTweet(
        content=request.tweet_data,
        author=user,
        attachments=medias,
        likes=[],
    )
    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)
    return tweet


async def set_tweet_like(
    tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession
) -> ErrorResponse | None:
    """Добавление лайка к твиту"""
    tweet = await get_tweet_by_id(tweet_id, session)
    if not tweet:
        return await error_handler(
            error=TweetNotFound(
                status=HTTPStatus.NOT_FOUND, message="Tweet not found"
            )
        )

    like = BaseLike(tweet=tweet, user=user, name=user.name)
    tweet.like_count += 1
    session.add(like)
    await session.commit()


async def del_tweet_like(
    tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession
) -> None:
    """Удаление лайка из твита"""
    tweet = await get_tweet_by_id(tweet_id, session)
    await delete_like_by_tweet_id_and_user_id(tweet_id, user.id, session)
    tweet.like_count -= 1
    await session.commit()


async def get_tweet_by_id(
    tweet_id: BaseTweet.id, session: AsyncSession
) -> BaseTweet | None:
    """Получение твита по id"""
    query = (
        select(BaseTweet)
        .options(selectinload(BaseTweet.author))
        .filter(BaseTweet.id == tweet_id)
    )
    result = await session.execute(query)
    return result.scalar()


async def delete_user_tweet(
    tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession
) -> ErrorResponse | None:
    """Удаление твита"""
    tweet = await get_tweet_by_id(tweet_id, session)
    if not tweet:
        return await error_handler(
            error=TweetNotFound(
                status=HTTPStatus.NOT_FOUND, message="Tweet not found"
            )
        )
    if tweet.author.id != user.id:
        return await error_handler(
            error=TweetNotOwnedByAuthor(
                status=HTTPStatus.FORBIDDEN,
                message="Tweet not owned by author",
            )
        )
    await session.delete(tweet)
    await session.commit()
