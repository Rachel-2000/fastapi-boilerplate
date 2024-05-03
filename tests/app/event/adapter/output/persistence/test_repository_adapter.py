from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.application.dto import EventDTO, EventDTOCreate
from app.event.domain.command import CreateEventCommand
from app.event.domain.entity.event import Event
from app.event.domain.repository.event_repository import EventRepository
from tests.support.user_fixture import make_event

event_repo_mock = AsyncMock(spec=EventRepository)
repository_adapter = EventRepositoryAdapter(event_repo=event_repo_mock)


@pytest.mark.asyncio
async def test_get_event_by_id(session: AsyncSession):
    # Given data for event
    id = 1
    title = "Test"
    description = "Test"
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
        invitees=["1", "2"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    event_repo_mock.get_event_by_id.return_value = eventDTO
    repository_adapter.event_repo = event_repo_mock

    # Mock result
    result = await repository_adapter.get_event_by_id(event_id=id)

    # Verify correctness
    assert result.id == eventDTO.id
    assert result.title == eventDTO.title
    assert result.status == eventDTO.status
    assert result.startTime == eventDTO.startTime
    assert result.endTime == eventDTO.endTime
    assert result.invitees == eventDTO.invitees
    repository_adapter.event_repo.get_event_by_id.assert_awaited_once_with(event_id = eventDTO.id)


@pytest.mark.asyncio
async def test_get_event_by_id_nonexist(session: AsyncSession):
    id = 1

    event_repo_mock.get_event_by_id.return_value = None
    repository_adapter.event_repo = event_repo_mock

    # Mock result
    result = await repository_adapter.get_event_by_id(event_id=id)

    # Verify correctness
    assert result is None


@pytest.mark.asyncio
async def test_create_event(session: AsyncSession):
    # Given
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
        invitees=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


    event_repo_mock.create_event.return_value = True
    repository_adapter.event_repo = event_repo_mock

    # When
    result = await repository_adapter.create_event(eventDTO=eventDTO)

    # Then
    assert result is True
    repository_adapter.event_repo.create_event.assert_awaited_once_with(eventDTO=eventDTO)


@pytest.mark.asyncio
async def test_delete_event_by_id(session: AsyncSession):
    id = 1

    event_repo_mock.delete_event_by_id.return_value = True
    repository_adapter.event_repo = event_repo_mock

    # When
    result = await repository_adapter.delete_event_by_id(event_id=id)

    # Then
    assert result is True
    repository_adapter.event_repo.delete_event_by_id.assert_awaited_once_with(event_id=id)


@pytest.mark.asyncio
async def test_delete_event_by_id_nonexist(session: AsyncSession):
    id = 1

    event_repo_mock.delete_event_by_id.return_value = False
    repository_adapter.event_repo = event_repo_mock

    # When
    result = await repository_adapter.delete_event_by_id(event_id=id)

    # Then
    assert result is False

