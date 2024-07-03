from fastapi import APIRouter, Depends
from app.api.core.pydantic_models import Follower, Following, UserResponse, UserProfile
from app.api.core.validators import verify_api_key
router = APIRouter()


@router.get("/users/me", response_model=UserResponse)
async def get_current_user(api_key: str = Depends(verify_api_key)):
    # Заглушка данных пользователя
    user_data = {
        "id": 1,
        "name": "leon",
        "followers": [
            Follower(id=2, name="john"),
            Follower(id=3, name="jane")
        ],
        "following": [
            Following(id=4, name="doe"),
            Following(id=5, name="smith")
        ]
    }

    return UserResponse(result=True, user=UserProfile(**user_data))
