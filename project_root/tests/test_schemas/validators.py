from fastapi import Header


def validate_api_key(api_key: str = Header(None)) -> bool:
    """Валидация API ключа."""
    if api_key != "test":
        raise ValueError
    return True


# , Q000, D400, I005, WPS, C812, B008
