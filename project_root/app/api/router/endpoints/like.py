from fastapi import APIRouter

router = APIRouter()


@router.get("/likes")
async def get_likes(): ...
