from fastapi import Header


def validate_api_key(api_key: str = Header(None)) -> bool:
    if api_key != "test":
        raise ValueError
    return True
