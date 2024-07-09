from http import HTTPStatus
import random

from sqlalchemy import select
from typing import List
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.db.base_models import Tweet as BaseTweet, User as BaseUser, Like as BaseLike, Media as BaseMedia
from app.api.core.pydantic_models import TweetSchema, TweetCreateRequest, TweetResponsePostSchema, ErrorResponse
from app.api.exceptions.error_handler import error_handler
from app.api.exceptions.models import TweetNotFound, TweetNotOwnedByAuthor
from app.api.services.like import get_like_by_tweet_id_and_user_id
from app.api.services.media import get_medias_from_base


async def create_tweets_flush(tweets: List[BaseTweet], session: AsyncSession) -> List[BaseTweet]:
    for tweet in tweets:
        session.add(tweet)
    await session.flush()
    return tweets


async def save_user_tweets_with_likes_and_media(tweets: List[BaseTweet],
                                                user: BaseUser,
                                                medias: List[str],
                                                session: AsyncSession) -> None:
    random_like = random.randint(0, 1)
    for tweet in tweets:
        tweet.author = user

        media_file = medias.pop()

        media = BaseMedia(tweet=tweet, tweet_data=media_file)  # await bytes_to_str(media_file))
        if random_like:
            like = BaseLike(tweet=tweet, user=user, name=user.name)
            tweet.like_count = 1
            session.add(like)
        session.add(media)
        random_like = random.randint(0, 1)


async def get_user_tweets(session: AsyncSession) -> Sequence[BaseTweet]:
    result = await session.execute(
        select(BaseTweet)
        .options(selectinload(BaseTweet.attachments))
        .options(selectinload(BaseTweet.likes).selectinload(BaseLike.user))
        .options(selectinload(BaseTweet.author))
    )
    return result.scalars().all()


async def tweets_as_schema(tweets: Sequence[BaseTweet]) -> List[TweetSchema]:
    tweet_schemas = [TweetSchema.model_validate(tweet) for tweet in tweets]
    return tweet_schemas


async def create_new_tweet(request: TweetCreateRequest,
                           user: BaseUser,
                           session: AsyncSession) -> TweetResponsePostSchema:
    medias = await get_medias_from_base(request.tweet_media_ids, session)
    tweet = BaseTweet(content=request.tweet_data,
                      author=user,
                      attachments=medias,
                      likes=[], )
    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)
    return TweetResponsePostSchema(tweet_id=tweet.id, result=True)


async def set_tweet_like(tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession) -> None:
    tweet = await get_tweet_by_id(tweet_id, session)
    if not tweet:
        return

    like = BaseLike(tweet=tweet, user=user, name=user.name)
    tweet.like_count += 1
    session.add(like)
    await session.commit()


async def del_tweet_like(tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession) -> None:
    tweet = await get_tweet_by_id(tweet_id, session)
    like = await get_like_by_tweet_id_and_user_id(tweet_id, user.id, session)
    tweet.like_count -= 1
    await session.delete(like)
    await session.commit()


async def get_tweet_by_id(tweet_id: BaseTweet.id, session: AsyncSession) -> BaseTweet | None:
    query = select(BaseTweet).options(selectinload(BaseTweet.author)).filter(BaseTweet.id == tweet_id)
    result = await session.execute(query)
    return result.scalar()


async def delete_user_tweet(tweet_id: BaseTweet.id, user: BaseUser, session: AsyncSession) -> ErrorResponse | None:
    tweet = await get_tweet_by_id(tweet_id, session)
    if not tweet:
        return await error_handler(error=TweetNotFound(status=HTTPStatus.NOT_FOUND, message="Tweet not found"))
    if tweet.author.id != user.id:
        return await error_handler(
            error=TweetNotOwnedByAuthor(status=HTTPStatus.FORBIDDEN, message="Tweet not owned by author"))
    await session.delete(tweet)
    await session.commit()
