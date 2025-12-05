from pydantic import BaseModel
from uuid import UUID
class GameResult(BaseModel):
    session_id: UUID
    score: int
    winner_id: int
    
class GameSession(BaseModel):
    session_id: UUID
    user_1: UUID
    user_2: UUID
    status: str
    winner_id: UUID
    game_score: UUID