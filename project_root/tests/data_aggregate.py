import os
from typing import Dict, List, Tuple
from sqlalchemy import select

from app.api.db.base_models import ApiKey, Tweet, User
from app.api.db.db import SessionManager
from app.api.services import api_key, follower, tweet, user
from tests.data_aggregate_models import api_keys
from tests.data_aggregate_models import media_str as m_str
from tests.data_aggregate_models import tweet_titles, users


async def create_instance_user(
    user_data: List[Dict[str, str | Dict[str, str]]]
) -> List[User]:
    """Инициализация пользователя"""
    users_list = [User(**usr) for usr in user_data]
    return users_list


async def create_instance_api_key(
    api_key_data: List[Dict[str, str]]
) -> List[ApiKey]:
    """Инициализация API ключей"""
    api_keys_list = [ApiKey(**key) for key in api_key_data]
    return api_keys_list


async def save_media_path(media: [List]) -> List[str]:
    """Сохраняет медиа-файлы в объект media"""
    path = os.path.join(os.getcwd(), "media")
    for folder in os.listdir(path):
        if os.path.isdir(f"{path}/{folder}"):
            for file in os.listdir(f"{path}/{folder}"):
                media.append(f"media/{folder}/{file}")
    return media


async def create_instance_tweets(
    titles: List[str],
) -> Tuple[List[List[Tweet]], List[Tweet]]:
    """Инициализация контента твитов"""
    twits = [Tweet(content=item) for item in titles]
    parse_tweets = await parser(twits)
    return parse_tweets, twits


async def parser(tweets: List[Tweet]) -> List[List[Tweet]]:
    """Разделение твитов на части"""
    length = len(tweets)
    part1 = tweets[: length // 3]
    part2 = tweets[length // 3: (length // 3) * 2]
    part3 = tweets[(length // 3) * 2:]
    return [part1, part2, part3]


async def init_test_data(manager: SessionManager) -> None:
    """Инициализация тестовых данных в базе данных"""
    async with manager.get_session() as session:
        users_list, keys, tweets, media = await main()
        parse_tweets, list_tweets = tweets
        for user_obj in users_list:
            tweet_obj = parse_tweets.pop()
            user_flush = await user.create_user_flush(user_obj, session)
            await api_key.save_user_api_key(
                keys.pop(), user_flush, session
            )
            list_tweets_flush = await tweet.create_tweets_flush(
                tweet_obj, session
            )
            await tweet.save_user_tweets_with_likes_and_media(
                list_tweets_flush, user_flush, media, session
            )

        await follower.save_user_followers(session)
        await session.commit()


async def check_aggregate_db(manager: SessionManager) -> bool:
    """Проверка существования данных в базе данных"""
    query = select(User).limit(1)
    async with manager.get_session() as session:
        result = await session.execute(query)
    return bool(result.scalar())


async def main() -> Tuple[
    List[User],
    List[ApiKey],
    Tuple[List[List[Tweet]], List[Tweet]],
    List[str],
]:
    """Инициализация тестовых данных в базе данных"""
    users_list = await create_instance_user(users)
    api_keys_list = await create_instance_api_key(api_keys)
    media_links = await save_media_path(m_str)
    tweets_tuple = await create_instance_tweets(tweet_titles)
    return users_list, api_keys_list, tweets_tuple, media_links
