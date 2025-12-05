from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING, List
import uuid
from datetime import datetime
from sqlalchemy import DateTime, func
from database import Base

if TYPE_CHECKING:
    from .team_db import Team_DB
    from .items_db import Items_DB
    from .refresh_token_db import RefreshToken_DB
    from .quest_bd import Quests_DB
    from .user_quests import UserQuests

def generate_uuid7():
    """Генератор UUID v7 (time-ordered UUID)"""
    return uuid.uuid4()

class User_DB(Base):
    __tablename__ = "users"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=generate_uuid7
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=0)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    energy: Mapped[int] = mapped_column(Integer, default=10)
    team_uid: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('teams.team_id'), 
        nullable=True
    )
    url: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="player")
    
    # ИЗМЕНИТЕ ВСЕ lazy="joined" НА lazy="select"
    team: Mapped[Optional['Team_DB']] = relationship('Team_DB', back_populates='users', lazy="select")
    items: Mapped[List['Items_DB']] = relationship('Items_DB', back_populates='user', lazy="select")
    
    # УБЕРИТЕ user_quests - используйте только quests
    # user_quests: Mapped[List['UserQuests']] = relationship(
    #     'UserQuests',
    #     back_populates='user',
    #     lazy="select"
    # )
    
    # Связь с квестами через association table
    quests: Mapped[List['Quests_DB']] = relationship(
        'Quests_DB',
        secondary='user_quests',
        back_populates='users',
        lazy="select",  # ИЗМЕНИТЬ С joined НА select
        viewonly=False  # Можете оставить True если не планируете добавлять quests напрямую
    )
    
    refresh_tokens: Mapped[List['RefreshToken_DB']] = relationship(
        'RefreshToken_DB', 
        back_populates='user',
        lazy="select"
    )