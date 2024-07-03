from fastapi import APIRouter

router = APIRouter()


@router.get("/followers")
async def get_followers():
    ...