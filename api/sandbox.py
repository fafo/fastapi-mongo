from fastapi import APIRouter, Depends, HTTPException

from services.users import fastapi_users
from services.spam import crudspam
from models.users import UserDB
from models.base  import SpamItem, SpamItemCreate

router = APIRouter()


@router.get("/test_open")
def test_open():
    return "ok"


@router.get("/test_restricted")
def test_restricted(user: UserDB = Depends(fastapi_users.get_current_user)):
    print("USER:", user)
    return "ok"


@router.post("/spam")
async def create_spam(item: SpamItemCreate):
    res = await crudspam.create(SpamItem(**item.dict()))
    return {"id": str(res)}


@router.get("/spam/{id}")
async def read_spam(id: str) -> SpamItem:
    res = await crudspam.read(id)
    if res:
        return res
    else:
        raise HTTPException(404, "spam not found")
