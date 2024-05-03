from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase
# from app.user.domain.entity.user import User
from core.db import Base
from core.db.mixins import TimestampMixin
from enum import Enum as PyEnum
from datetime import datetime
from typing import List

# Define an association table for the many-to-many relationship between Event and User
event_user_association_table = Table(
    'event_user_association',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

class EventStatus(PyEnum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

class Event(Base, TimestampMixin):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255))
    status = Column(Enum(EventStatus), nullable=False)
    # createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    
    # # Define a relationship to the User entity for invitees
    invitees: Mapped[List["User"]] = relationship(
        secondary=event_user_association_table,
        back_populates="events",
        cascade="all, delete")

    @classmethod
    def create(
            cls, *, title: str, description: str, status: Enum(EventStatus),
            created_at: datetime, updated_at: datetime, startTime: datetime, endTime: datetime, invitees: List["User"]
    ) -> "Event":
        return cls(
            title=title,
            description=description,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            startTime=startTime,
            endTime=endTime,
            invitees=invitees
        )

