from fastapi import APIRouter

router = APIRouter()


@router.get("/twits")
async def get_twits():
    ...