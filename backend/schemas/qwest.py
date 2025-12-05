from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

class UserQuestBase(BaseModel):
    user_id: uuid.UUID
    quest_id: uuid.UUID
    progress: int = 0
    status: str = "isnt active"
    started_at: Optional[datetime] = None

class QuestCreate(BaseModel):
    name: str
    type: str
    description: str
    amount: int

class UserQuestCreate(BaseModel):
    quest_id: uuid.UUID

class QuestResponse(BaseModel):
    quest_id: uuid.UUID
    name: str
    type: str
    description: str
    amount: int
    users: List[dict] = []
    
    class Config:
        from_attributes = True
        
class QuestSetProgress(BaseModel):
    quest_id: uuid.UUID
    progress: int

class QuestSetStatus(BaseModel):
    quest_id: uuid.UUID
    status: str