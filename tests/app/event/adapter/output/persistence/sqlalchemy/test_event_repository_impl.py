from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.adapter.output.persistence.sqlalchemy.event_repository_impl import EventSQLAlchemyRepo
from app.event.application.dto import EventDTO, EventDTOCreate
from app.event.domain.entity.event import Event
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.domain.entity.user import User
from tests.support.user_fixture import make_event, make_user

event_repo = EventSQLAlchemyRepo()
user_repo = UserSQLAlchemyRepo()


@pytest.mark.asyncio
async def test_get_event_by_id(session: AsyncSession):
    # Given
    id = 101
    title = "Test"
    description = "Test"
    status = "TODO"
    startTime = datetime.now()
    endTime = datetime.now()

    # eventDTO = EventDTO(
    #     id=id,
    #     title=title,
    #     description=description,
    #     status=status,
    #     startTime=startTime,
    #     endTime=endTime,
    #     invitees=["1", "2"],
    #     created_at=datetime.now().replace(minute=0, second=0, microsecond=0),
    #     updated_at=datetime.now().replace(minute=0, second=0, microsecond=0)
    # )

    event = make_event(
        id=id,
        title=title,
        description=description,
        status=status,
        startTime=startTime,  # set precision to hour
        endTime=endTime
    )

    session.add(event)
    await session.commit()

    # When
    res1 = await event_repo.get_event_by_id(event_id=id)

    # Then
    assert res1.id == event.id
    assert res1.title == event.title
    assert res1.status == event.status
    assert res1.startTime.replace(minute=0, second=0, microsecond=0) == event.startTime.replace(minute=0, second=0, microsecond=0)
    assert res1.endTime.replace(minute=0, second=0, microsecond=0) == event.endTime.replace(minute=0, second=0, microsecond=0)

    await session.delete(event)
    await session.commit()


@pytest.mark.asyncio
async def test_create_event(session: AsyncSession):
    # Given
    # event = make_event(
    #     id=1,
    #     title="TestTitle2",
    #     description="TestDescription2",
    #     status="TODO",
    #     startTime=datetime.now(),
    #     endTime=datetime.now()
    # )

    title = "Test"
    description = "Test"
    status = "TODO"
    startTime = datetime.now()
    endTime = datetime.now()

    eventDTO = EventDTOCreate(
        title=title,
        description=description,
        status=status,
        startTime=startTime,
        endTime=endTime,
        invitees=["1", "2"],
        created_at=datetime.now().replace(minute=0, second=0, microsecond=0),
        updated_at=datetime.now().replace(minute=0, second=0, microsecond=0)
    )

    # When
    res = await event_repo.create_event(eventDTO=eventDTO)

    # Then
    assert res is True


@pytest.mark.asyncio
async def test_delete_event_by_id(session: AsyncSession):
    # Given
    id = 2
    event = make_event(
        id=id,
        title="TestTitle1",
        description="TestDescription",
        status="TODO",
        startTime=datetime.now(),
        endTime=datetime.now()
    )
    session.add(event)
    await session.commit()

    # When
    res = await event_repo.delete_event_by_id(event_id=id)

    # Then
    assert res is True


@pytest.mark.asyncio
async def test_merge_all_overlapping_events(session: AsyncSession):
    # Given
    user_1 = make_user(
                id = 101,
                password="password",
                email="a@b.c",
                nickname="hide",
                is_admin=True,
                lat=37.123,
                lng=127.123,
            )
    # user_2 = make_user(
    #             password="password2",
    #             email="b@b.c",
    #             nickname="test",
    #             is_admin=False,
    #             lat=37.123,
    #             lng=127.123,
    #         )
    session.add(user_1)
    await session.commit()

    event_1 = Event(
        title="Event 1",
        description="Description 1",
        status="TODO",
        startTime=datetime(2024, 1, 1, 10, 0, 0),
        endTime=datetime(2024, 1, 1, 11, 0, 0),
        invitees=[user_1]
    )
    event_2 = Event(
        title="Event 2",
        description="Description 2",
        status="IN_PROGRESS",
        startTime=datetime(2024, 1, 1, 10, 30, 0),
        endTime=datetime(2024, 1, 1, 12, 0, 0),
        invitees=[user_1]
    )


    session.add_all([event_1, event_2])
    # session.add(event_2)
    await session.commit()

    # When
    merged_events = await event_repo.merge_all_overlapping_events(user_id=101)

    # Then
    assert len(merged_events) == 1
    assert merged_events[0].title == "Event 1 + Event 2"
    assert merged_events[0].description == "Description 1 ; Description 2"
    assert merged_events[0].status == "IN_PROGRESS"
    assert merged_events[0].startTime == datetime(2024, 1, 1, 10, 0, 0)
    assert merged_events[0].endTime == datetime(2024, 1, 1, 12, 0, 0)

    await session.delete(event_1)
    await session.delete(event_2)
    await session.delete(user_1)
    await session.commit()