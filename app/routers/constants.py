from fastapi import APIRouter


router = APIRouter()


@router.get("/constants")
async def values():
    return {"result": "hi"}
