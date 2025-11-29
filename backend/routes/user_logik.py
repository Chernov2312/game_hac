from fastapi import APIRouter, HTTPException, Depends
from database.models import User_DB, Casino_DB, Items_DB
from database import BaseDao
import random
from schemas import Prize, get_prize, User_Bet
from core import decode_access_token
user_router = APIRouter()

user_basedao = BaseDao(User_DB)
casino_basedao = BaseDao(Casino_DB)
items_dao = BaseDao(Items_DB)

@user_router.get("/profile/balance")
async def get_user_amount(user: User_DB = Depends(decode_access_token)):
    return {
        "amount": user.amount,
        "currency_symbol": random.choice(["❄️", "💰", "$", "RUB"])
    }
    
@user_router.get("/profile/me")
async def get_user_info(user: User_DB = Depends(decode_access_token)):
    return {"items": user.items}