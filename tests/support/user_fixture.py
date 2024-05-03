from datetime import datetime
from enum import Enum

from app.event.domain.entity.event import EventStatus, Event
from app.user.domain.entity.user import User
from app.user.domain.vo.location import Location


def make_user(
    id: int | None = None,
    password: str = "password",
    email: str = "h@id.e",
    nickname: str = "hide",
    is_admin: bool = False,
    lat: float = 37.123,
    lng: float = 127.123,
):
    return User(
        id=id,
        password=password,
        email=email,
        nickname=nickname,
        is_admin=is_admin,
        location=Location(lat=lat, lng=lng),
    )

def make_event(
    id: int | None = None,
    title: str = "Test Event",
    description: str = "Test Description",
    status: EventStatus = "TODO",
    created_at: datetime = datetime.now(),
    updated_at: datetime = datetime.now(),
    startTime: datetime = datetime.now(),
    endTime: datetime = datetime.now()
):
    return Event(
        id = id,
        title = title,
        description = description,
        status = status,
        created_at = created_at,
        updated_at = updated_at,
        startTime = startTime,
        endTime = endTime
    )
