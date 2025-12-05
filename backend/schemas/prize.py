from pydantic import BaseModel
from .user import User
class Prize(BaseModel):
    name: str
    type: str
    description: str
    amount: int = 0
    amoji: str = ""
    color: str = ""
    
    rare: str
    
    
class GetPrize(BaseModel):
    name: str

class UserWin(BaseModel):
    username: str
    
class UserBet(BaseModel):
    bet: int