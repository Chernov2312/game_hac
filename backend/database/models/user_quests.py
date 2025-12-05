from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING, List
import uuid
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB
    from .quest_bd import Quests_DB


class UserQuests(Base):
    __tablename__ = 'user_quests'
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.user_id', ondelete='CASCADE'),
        primary_key=True
    )
    
    quest_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('quests.quest_id', ondelete='CASCADE'),
        primary_key=True
    )
    
    progress: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="isnt active")
    started_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # УБЕРИТЕ ЭТИ ОТНОШЕНИЯ - они конфликтуют с secondary связями
    # user: Mapped["User_DB"] = relationship(back_populates="user_quests")
    # quest: Mapped["Quests_DB"] = relationship(back_populates="user_quests")