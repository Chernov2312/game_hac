from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING, List
import uuid
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB
    
class Quests_DB(Base):
    __tablename__ = "quests"
    
    quest_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    
    
    # УБЕРИТЕ user_quests отношение
    # user_quests: Mapped[List['UserQuests']] = relationship(
    #     'UserQuests',
    #     back_populates='quest',
    #     lazy="select"
    # )
    
    # Связь с пользователями через association table
    users: Mapped[List['User_DB']] = relationship(
        'User_DB',
        secondary='user_quests',
        back_populates='quests',
        lazy="select",  # ИЗМЕНИТЬ С joined НА select
        viewonly=False
    )