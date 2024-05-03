from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, composite, relationship, DeclarativeBase

from app.user.domain.vo.location import Location
from core.db import Base
from core.db.mixins import TimestampMixin

from typing import List
from sqlalchemy.ext.mutable import MutableList
from app.event.domain.entity.event import event_user_association_table, Event


# association_table = Table('association', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('event_id', Integer, ForeignKey('events.id'))
# )


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    events: Mapped[List[Event]] = relationship(
        secondary=event_user_association_table,
        back_populates="invitees")
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    location: Mapped[Location] = composite(mapped_column("lat"), mapped_column("lng"))

    @classmethod
    def create(
        cls, *, email: str, password: str, nickname: str, location: Location
    ) -> "User":
        return cls(
            email=email,
            password=password,
            nickname=nickname,
            is_admin=False,
            location=location,
        )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="USER ID")
    # name: str = Field(..., title="Username")
    email: str = Field(..., title="Email")
    nickname: str = Field(..., title="Nickname")
