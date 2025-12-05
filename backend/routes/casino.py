from fastapi import APIRouter, HTTPException, Depends
from database.models import User_DB, Casino_DB, Items_DB
from database import BaseDao
import random
from schemas import Prize, GetPrize, UserBet, BetResultResponse
from core import get_random_item, decode_access_token
from typing import List
casino_router = APIRouter()

user_basedao = BaseDao(User_DB)
casino_basedao = BaseDao(Casino_DB)
items_dao = BaseDao(Items_DB)


@casino_router.get("/prizes", tags=["not_for_game"])
async def get_prizes_to_front() -> List[Prize]:
    casino = await casino_basedao.get_entities()
    return casino
    
@casino_router.post("/add_prize", tags=["not_for_game"])
async def add_prize_db(prize: Prize):
    casino = await casino_basedao.get_by_name(prize.name)
    if casino is None:
        await casino_basedao.create_entity(prize.model_dump())
        return {"message": "success"}
    prize.amount += casino.amount
    await casino_basedao.update_entity(casino.item_id, prize.model_dump())
    return {"message": "success"}

@casino_router.get("/user/balance", tags=["user"])
async def get_user_balance(user: User_DB = Depends(decode_access_token)):
    return {
        "amount": user.amount,
        "currency_symbol": random.choice(["❄️", "💰", "$", "RUB"])
    }

@casino_router.post("/spin", tags=["spin"])
async def user_win_to_db(
    bet: UserBet,
    user: User_DB = Depends(decode_access_token)
    ) -> BetResultResponse:
    if user.amount < bet.bet:
        raise HTTPException(status_code=402, detail={
            "error_code": "insufficient_funds",
            "message": "Не хватает монет для ставки"
        })
    if bet.bet <= 10:
        raise HTTPException(status_code=402, detail={
            "error_code": "insufficient_funds",
            "message": "Ставка слишком мала"
        })
    win = await get_random_item()
    items_dao.create_entity({"user_id":user.user_id, "casino_id":win["item"].casino_id, "status":True})
    user.amount -= bet.bet
    user.amount += win["item"].amount
    user_basedao.update_entity(user.user_id, user.__dict__)
    return {
        "winner":{
            "id":win["item"].item_id,
            "name":win["item"].casino_id,
            "description": win["item"].description,
            "type": win["item"].type,
            "amount": win["item"].amount,
            "emoji":win["item"].amoji,
            "color_hex": win["itog_rare"]
        },
        "new_balance": user.money
    }