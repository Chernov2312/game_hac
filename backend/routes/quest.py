from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header

from core import decode_role, get_time_diff_seconds, decode_access_token
from database.models import User_DB, Token_qr_DB, Quests_DB, UserQuests
from database.basedao import BaseDao
from schemas import QuestCreate, UserQuestCreate, CreateSuccess, QuestSetStatus, QuestSetProgress, QuestResponse
from uuid import UUID
from typing import List

quest_router = APIRouter()
user_basedao = BaseDao(User_DB)
quest_dao = BaseDao(Quests_DB)
user_qwests_dao = BaseDao(UserQuests)


@quest_router.post("/create/qwest", tags=["quest"])
async def create_qwest(quest: QuestCreate) -> QuestCreate:
    quest = await quest_dao.create_entity(quest.model_dump())
    return quest


@quest_router.post("/user/add", tags=["quest"])
async def user_add_quest(quest_id: UserQuestCreate, user: User_DB = Depends(decode_access_token)) -> CreateSuccess:
    user_quest = await user_qwests_dao.create_entity({"user_id": user.user_id, "quest_id": quest_id.quest_id, "status": "active"})
    return {
        "user_id": user_quest.user_id,
        "qwest_id": user_quest.quest_id,
        "status": "active"
    }


@quest_router.put("/set/status", tags=["quest"])
async def quest_set_status(quest: QuestSetStatus, user: User_DB = Depends(decode_access_token)) -> QuestSetStatus:
    user_quest: UserQuests = await user_qwests_dao.get_entity_by_id(quest.quest_id)
    user_quest = quest.status
    await user_qwests_dao.update_entity(user_quest.quest_id, user_quest.__dict__)
    return {
            "quest_id": quest.quest_id,
            "status": quest.status
            }
    
@quest_router.put("/set/progress", tags=["quest"])
async def quest_set_progress(quest: QuestSetProgress, user: User_DB = Depends(decode_access_token)) -> QuestSetStatus:
    user_quest: UserQuests = await user_qwests_dao.get_entity_by_id(quest.quest_id)
    user_quest = quest.progress
    await user_qwests_dao.update_entity(user_quest.quest_id, user_quest.__dict__)
    return {
            "quest_id": quest.quest_id,
            "status": quest.progress
            }

@quest_router.get("/get/user/quests", response_model=List[QuestResponse], tags=["quest"])
async def get_user_quests(user: User_DB = Depends(decode_access_token)):
    return [
        QuestResponse(
            quest_id=quest.quest_id,
            user_id=user.user_id,
            name=quest.name,
            description=quest.description,
            amount=quest.amount
        )
        for quest in user.quests
    ]