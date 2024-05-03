from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.application.dto import EventDTO

from app.event.application.service.event_service import EventService
from app.event.domain.command import CreateEventCommand
from app.event.domain.entity.event import Event
from tests.support.user_fixture import make_event

repository_mock = AsyncMock(spec=EventRepositoryAdapter)
event_service = EventService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_event_by_id():
    # Given
    id = 1
    # event = make_event(
    #     id=id,
    #     title="TestTitle1",
    #     description="TestDescription1",
    #     status="TODO",
    #     startTime=datetime.now,
    #     endTime=datetime.now
    # )
    eventDTO = EventDTO(
        id=id,
        title="TestTitle1",
        description="TestDescription1",
        status="TODO",
        startTime=datetime.now(),
        endTime=datetime.now(),
        invitees=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    repository_mock.get_event_by_id.return_value = eventDTO
    event_service.repository = repository_mock

    # Then
    result = await event_service.get_event_by_id(id=id)

    # Verify correctness
    assert result.id == eventDTO.id
    assert result.title == eventDTO.title
    assert result.status == eventDTO.status
    assert result.startTime == eventDTO.startTime
    assert result.endTime == eventDTO.endTime


@pytest.mark.asyncio
async def test_create_event():
    # Given
    command = CreateEventCommand(
        id=1,
        title="TestTitle2",
        description="TestDescription2",
        status="TODO",
        startTime=datetime.now(),
        endTime=datetime.now()
    )

    repository_mock.create_event.return_value = True
    event_service.repository = repository_mock

    # When
    result = await event_service.create_event(command=command)

    # Then
    assert result is True


@pytest.mark.asyncio
async def test_create_event_duplicated():
    # Given
    id = 1
    title = "DuplicateTest"
    description = "TestDescription"
    status = "TODO"
    startTime = datetime.now()
    endTime = datetime.now()

    eventDTO = EventDTO(
        id=id,
        title=title,
        description=description,
        status=status,
        startTime=startTime,
        endTime=endTime,
        invitees=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    command = CreateEventCommand(
        id=id,
        title=title,
        description=description,
        status=status,
        startTime=startTime,
        endTime=endTime
    )

    repository_mock.get_event_by_id.return_value = eventDTO
    repository_mock.create_event.return_value = False
    event_service.repository = repository_mock

    # When
    result = await event_service.create_event(command=command)

    # Then
    assert result is False
    # await event_service.delete_event_by_id(event_id=id)


@pytest.mark.asyncio
async def test_delete_event_by_id():
    id = 1

    repository_mock.delete_event_by_id.return_value = True
    event_service.repository = repository_mock

    # When
    result = await event_service.delete_event_by_id(event_id=id)

    # Then
    assert result is True


@pytest.mark.asyncio
async def test_delete_event_by_id_nonexist():
    id = 1

    repository_mock.delete_event_by_id.return_value = False
    event_service.repository = repository_mock

    # When
    result = await event_service.delete_event_by_id(event_id=id)

    # Then
    assert result is False

