import os
from typing import Dict, List, Tuple
import aiofiles
from tests.data_aggregate_models import media_str as m_str, users, tweet_titles, api_keys
from app.api.db.base_models import (
    ApiKey,
    Follower,
    Media,
    Tweet,
    User,
)


async def create_instance_user(user_data: List[Dict[str, str | Dict[str, str]]]) -> List[User]:
    users_list = [User(**user) for user in user_data]
    return users_list


async def create_instance_api_key(api_key_data: List[Dict[str, str]]) -> List[ApiKey]:
    api_keys_list = [ApiKey(**api_key) for api_key in api_key_data]
    return api_keys_list


async def create_instance_followers(users_list: List[User]) -> List[Follower]:
    followers = []
    while users_list:
        user = users_list.pop()
        for inx in range(len(users_list)):
            followers.append(Follower(follower=user, following=users_list[inx]))
    return followers


async def save_media_binary(media: Dict[str, List]) -> Dict[str, List[bytes]]:
    path = os.path.join(os.getcwd(), "/media")
    for folder in os.listdir(path):
        if os.path.isdir(f"{path}/{folder}"):
            for file in os.listdir(f"{path}/{folder}"):
                async with aiofiles.open(f"{path}/{folder}/{file}", mode="rb") as f:
                    file_content = await f.read()
                    if file.endswith(".gif"):
                        media["gif"].append(file_content)
                    elif file.endswith(".mp4"):
                        media["video"].append(file_content)
                    else:
                        media["image"].append(file_content)

    return media


async def save_media_for_tweets(media_bytes: Dict[str, List[bytes]]) -> List[Media]:
    return [Media(tweet_data=item) for media_type in media_bytes for item in media_bytes[media_type]]


async def create_instance_tweets(medias: List[Media], titles: List[str]) -> Tuple[List[List[Tweet]], List[Tweet]]:
    twits = [Tweet(content=item, attachments={"media": medias.pop()}) for item in titles if medias]
    parse_tweets = await parser(twits)
    return parse_tweets, twits


async def parser(tweets: List[Tweet]) -> List[List[Tweet]]:
    length = len(tweets)
    part1 = tweets[:length // 3]
    part2 = tweets[length // 3:(length // 3) * 2]
    part3 = tweets[(length // 3) * 2:]
    return [part1, part2, part3]


async def main() -> Tuple[List[User], List[ApiKey], List[Follower], Tuple[List[List[Tweet]], List[Tweet]]]:
    users_list = await create_instance_user(users)
    users_copy = users_list.copy()
    api_keys_list = await create_instance_api_key(api_keys)
    followers = await create_instance_followers(users_copy)
    media_binary = await save_media_binary(m_str)
    media_list = await save_media_for_tweets(media_binary)
    tweets_tuple = await create_instance_tweets(media_list, tweet_titles)
    return users_list, api_keys_list, followers, tweets_tuple
