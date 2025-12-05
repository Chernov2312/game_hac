from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Any,Dict
from uuid import UUID

class WinnerItemResponse(BaseModel):
    id: UUID = Field(description="UUID предмета")
    name: str = Field(description="Название предмета")
    description: Optional[str] = Field(None, description="Описание предмета")
    type: Literal["item", "currency", "boost", "skin"] = Field(description="Тип предмета")
    amount: int = Field(description="Количество/стоимость предмета")
    emoji: str = Field(description="Emoji представление предмета")
    color_hex: str = Field(description="Цвет в HEX формате (например, #FFD700)")

class BetResultResponse(BaseModel):
    winner: WinnerItemResponse = Field(description="Выигранный предмет")
    new_balance: int = Field(description="Новый баланс пользователя")

class UserBalance(BaseModel):
    amount: int = Field(description="Количество валюты")
    currency_symbol: str = Field(description="Символ валюты")

class UserResponse(BaseModel):
    id: UUID = Field(description="UUID пользователя")
    username: str = Field(description="Имя пользователя")
    department: Optional[str] = Field(None, description="Отдел/команда")
    avatar_url: Optional[str] = Field(None, description="URL аватара")
    level: int = Field(description="Уровень пользователя")
    xp: int = Field(description="Текущий опыт")
    max_xp: int = Field(description="Максимальный опыт для текущего уровня")
    inventory: List[Any] = Field(default_factory=list, description="Инвентарь пользователя")
    
class UserBalance(BaseModel):
    amount: int
    currency_symbol: str
    
class GameStart(BaseModel):
    session: UUID
    user_1: UUID
    user_2: UUID
    
class Redeem(BaseModel):
    status: str
    user_id: UUID
    item_id: UUID
    
    
class TeamLeaderboardEntry(BaseModel):
    """Запись в таблице лидеров команд"""
    username: str = Field(description="Название команды")
    max_score: int = Field(description="Максимальный счет команды")
    amount: int = Field(description="Баланс команды")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "Alpha Team",
                "max_score": 12500,
                "amount": 5000
            }
        }

class TeamLeaderboardResponse(BaseModel):
    """Ответ с лидербордом команд"""
    leaders: List[TeamLeaderboardEntry] = Field(description="Топ 10 команд")
    
    class Config:
        json_schema_extra = {
            "example": {
                "leaders": [
                    {"username": "Team Alpha", "max_score": 15000, "amount": 7500},
                    {"username": "Beta Squad", "max_score": 12000, "amount": 6000},
                ]
            }
        }
        
class CreateSuccess(BaseModel):
    user_id: UUID
    quest_id: UUID
    
class Quest(BaseModel):
    id: int
    name: str
    description: str
    reward: int
    completed: bool = False

class Balance(BaseModel):
    amount: int
    currency_symbol: str = "❄️"

class Energy(BaseModel):
    current: int
    max: int = 10
    next_refill_in_seconds: Optional[int] = None

class UserSummary(BaseModel):
    id: int = Field(alias="user_id")  # Используем alias для соответствия с полем БД
    display_name: str
    balance: Balance
    energy: Energy

    class Config:
        # Разрешаем использовать как field_name, так и alias при создании
        allow_population_by_field_name = True

class MainInfoResponse(BaseModel):
    user_summary: UserSummary
    quests: List[Dict[str, Any]] = []