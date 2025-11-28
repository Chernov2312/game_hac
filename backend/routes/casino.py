from fastapi import APIRouter, HTTPException
from database.models import User_DB, Casino_DB
from database import BaseDao

from schemas import Prize, get_prize, User_Win

casino_router = APIRouter()
user_basedao = BaseDao(User_DB)
casino_basedao = BaseDao(Casino_DB)

@casino_router.get("/prize")
async def get_prize_to_front(prize: get_prize):
    casino = await casino_basedao.get_by_name(prize.name)
    if not casino:
        raise HTTPException(status_code=404, detail="Prize not found")
    casino.amount -= 1
    await casino_basedao.update_entity(casino.item_id, casino.__dict__)
    return casino
    
@casino_router.post("/add_prize")
async def add_prize_db(prize: Prize):
    casino = await casino_basedao.get_by_name(prize.name) is None
    if casino is None:
        await casino_basedao.create_entity(prize.model_dump())
        return {"message": "success"}
    prize.amount += casino.amount
    await casino_basedao.update_entity(casino.item_id, prize.model_dump())


@casino_router.post("/add_prize")
async def add_prize_to_user(prize: Prize):
    casino = await casino_basedao.get_by_name(prize.name) is None
    if casino is None:
        await casino_basedao.create_entity(prize.model_dump())
        return {"message": "success"}
    prize.amount += casino.amount
    await casino_basedao.update_entity(casino.item_id, prize.model_dump())
    
@casino_router.post("/user_win")
async def user_win_to_db(user_win: User_Win):
    ...