from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.domain.entity.event import event_user_association_table, Event
from app.server import app
from app.event.adapter.output.persistence.sqlalchemy.event_repository_impl import EventSQLAlchemyRepo


from tests.support.token import USER_ID_1_TOKEN
from tests.support.user_fixture import make_event, make_user
#
# HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_event_by_id(session: AsyncSession):
    # Given
    id = 1
    startTime = datetime.now().replace(minute=0, second=0, microsecond=0)
    endTime = datetime.now().replace(minute=0, second=0, microsecond=0)
    created_at = datetime.now().replace(minute=0, second=0, microsecond=0)
    updated_at = datetime.now().replace(minute=0, second=0, microsecond=0)

    event = make_event(
        id=id,
        title="TestTitle1",
        description="TestDescription1",
        status="TODO",
        startTime=startTime,
        endTime=endTime,
        created_at=created_at,
        updated_at=updated_at
    )

    session.add(event)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/event/1")

    await session.delete(event)
    await session.commit()

    # Then
    res = response.json()
    assert res == {
        "id":id,
        "title":"TestTitle1",
        "description":"TestDescription1",
        "status":"TODO",
        "startTime":startTime.isoformat(),
        "endTime":endTime.isoformat(),
        "created_at":created_at.isoformat(),
        "updated_at":updated_at.isoformat(),
        "invitees":[]
    }


# @pytest.mark.asyncio
# async def test_get_event_by_id_nonexist(session: AsyncSession):
#
#     # When
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/api/v1/event/0")
#
#     # Then
#     assert response.status_code == 404


# No need since title can be duplicated
# @pytest.mark.asyncio
# async def test_create_event_duplicated(session: AsyncSession):
#     # Given
#     id = 1
#     startTime = datetime.now().replace(minute=0, second=0, microsecond=0).isoformat()
#     endTime = datetime.now().replace(minute=0, second=0, microsecond=0).isoformat()
#     created_at = datetime.now().replace(minute=0, second=0, microsecond=0)
#     updated_at = datetime.now().replace(minute=0, second=0, microsecond=0)
#
#     event = make_event(
#         id=id,
#         title="TestTitle1",
#         description="TestDescription1",
#         status="TODO",
#         startTime=startTime,
#         endTime=endTime,
#         created_at=created_at,
#         updated_at=updated_at
#     )
#     session.add(event)
#     await session.commit()
#
#     body = {
#         "title":"TestTitle1",
#         "description":"TestDescription1",
#         "status":"TODO",
#         "startTime":startTime,
#         "endTime":endTime,
#     }
#
#     # When
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/api/v1/event/", json=body)
#
#     # Then
#     assert response.status_code == 200
#     assert response.json() == False


@pytest.mark.asyncio
async def test_create_event(session: AsyncSession):
    # Given
    startTime = datetime.now().replace(minute=0, second=0, microsecond=0).isoformat()
    endTime = datetime.now().replace(minute=0, second=0, microsecond=0).isoformat()
    body = {
        "title": "TestTitle1",
        "description": "TestDescription1",
        "status": "TODO",
        "startTime": startTime,
        "endTime": endTime,
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/event/", json=body)

    # Then
    assert response.json() == True


@pytest.mark.asyncio
async def test_delete_event_by_id(session: AsyncSession):
    # Given
    id = 1
    startTime = datetime.now().replace(minute=0, second=0, microsecond=0)
    endTime = datetime.now().replace(minute=0, second=0, microsecond=0)
    created_at = datetime.now().replace(minute=0, second=0, microsecond=0)
    updated_at = datetime.now().replace(minute=0, second=0, microsecond=0)

    event = make_event(
        id=id,
        title="TestTitle1",
        description="TestDescription1",
        status="TODO",
        startTime=startTime,
        endTime=endTime,
        created_at=created_at,
        updated_at=updated_at
    )

    session.add(event)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/api/v1/event/1")

    # Then
    assert response.json() == True


@pytest.mark.asyncio
async def test_delete_event_by_id_nonexist(session: AsyncSession):

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/api/v1/event/0")

    # Then
    assert response.json() == False


@pytest.mark.asyncio
async def test_update_event(session: AsyncSession):
    # Given
    user_1 = make_user(
        id=100,
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
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/api/v1/event/merge-all/100")

    # Then
    resp = response.json()
    assert len(resp) == 1

