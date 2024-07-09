import random

from sqlalchemy import select
from typing import List, Dict, Any
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.db.base_models import Tweet as BaseTweet, User as BaseUser, Like as BaseLike, Media as BaseMedia
from app.api.core.pydantic_models import TweetSchema, TweetCreateRequest, TweetResponsePostSchema
from app.api.services.media import bytes_to_str, get_medias_from_base


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

        media = BaseMedia(tweet=tweet, tweet_data=media_file) #await bytes_to_str(media_file))
        if random_like:
            like = BaseLike(tweet=tweet, user=user, name=user.name)
            tweet.like_count = 1
            session.add(like)
        session.add(media)
        random_like = random.randint(0, 1)


async def get_user_tweets(user_id: BaseUser.id, session: AsyncSession) -> Sequence[BaseTweet]:
    result = await session.execute(
        select(BaseTweet)
        .options(selectinload(BaseTweet.attachments))
        .options(selectinload(BaseTweet.likes).selectinload(BaseLike.user))
        .options(selectinload(BaseTweet.author)).filter(BaseTweet.user_id == user_id)
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
                      likes=[],)
    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)
    return TweetResponsePostSchema(tweet_id=tweet.id, result=True)
