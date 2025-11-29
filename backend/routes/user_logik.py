from fastapi import APIRouter, HTTPException, Depends
from database.models import User_DB, Casino_DB, Items_DB
from database import BaseDao
import random
from schemas import Prize, get_prize, User_Bet, Redact_User
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
    return {
  "id": user.user_id,
  "username": user.username,
  "department": user.team,
  "avatar_url": user.url,
  "level": user.level,
  "xp": user.score,
  "max_xp": user.max_score,
  "inventory": user.items
}

@user_router.patch("/profile/me")
async def patch_user(redact_info: Redact_User, user: User_DB = Depends(decode_access_token)):
    user.display_name = redact_info.display_name
    user.url = redact_info.url
    await user_basedao.update_entity(user.id, user)
    return user

@user_router.get("/profile/inventory/{id}/code")
async def get_qr(id: int):
    return {
        "redeem_token": "secure-random-string-123",
        "expires_in_seconds": 300
    }