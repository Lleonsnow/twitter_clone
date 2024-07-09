import os
from typing import Dict, List, Tuple
import aiofiles
from tests.data_aggregate_models import media_str as m_str, users, tweet_titles, api_keys
from app.api.db.base_models import (
    ApiKey,
    Tweet,
    User,
)


async def create_instance_user(user_data: List[Dict[str, str | Dict[str, str]]]) -> List[User]:
    users_list = [User(**user) for user in user_data]
    return users_list


async def create_instance_api_key(api_key_data: List[Dict[str, str]]) -> List[ApiKey]:
    api_keys_list = [ApiKey(**api_key) for api_key in api_key_data]
    return api_keys_list


async def save_media_binary(media: [List]) -> List[str]:
    path = os.path.join(os.getcwd(), "media")
    for folder in os.listdir(path):
        if os.path.isdir(f"{path}/{folder}"):
            for file in os.listdir(f"{path}/{folder}"):
                media.append(f"{path}/{folder}/{file}")
    return media


# async def save_media_for_tweets(media_bytes: Dict[str, List[bytes]]) -> List[Media]:
#     return [Media(tweet_data=item) for media_type in media_bytes for item in media_bytes[media_type]]


async def create_instance_tweets(titles: List[str]) -> Tuple[List[List[Tweet]], List[Tweet]]:
    twits = [Tweet(content=item) for item in titles]
    parse_tweets = await parser(twits)
    return parse_tweets, twits


async def parser(tweets: List[Tweet]) -> List[List[Tweet]]:
    length = len(tweets)
    part1 = tweets[:length // 3]
    part2 = tweets[length // 3:(length // 3) * 2]
    part3 = tweets[(length // 3) * 2:]
    return [part1, part2, part3]


async def main() -> Tuple[List[User], List[ApiKey], Tuple[List[List[Tweet]], List[Tweet]], List[str]]:
    users_list = await create_instance_user(users)
    api_keys_list = await create_instance_api_key(api_keys)
    media_links = await save_media_binary(m_str)
    # media_list = await save_media_for_tweets(media_binary)
    tweets_tuple = await create_instance_tweets(tweet_titles)
    return users_list, api_keys_list, tweets_tuple, media_links
