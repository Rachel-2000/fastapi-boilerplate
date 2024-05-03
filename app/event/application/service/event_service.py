from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.application.dto import EventDTO, EventDTOCreate
from app.event.domain.command import CreateEventCommand
from app.event.domain.repository.event_repository import EventRepository
from app.event.domain.entity.event import Event
from app.event.domain.usecase.event import EventUseCase
from core.db import Transactional
from typing import List
from fastapi import HTTPException


class EventService(EventUseCase):
    def __init__(self, repository: EventRepositoryAdapter):
        self.event_repository = repository

    @Transactional()
    # async def create_event(self, command: CreateEventCommand) -> Event:
    async def create_event(self, command: CreateEventCommand) -> bool:
        # Validate event_data
        # event = Event(**command.model_dump())
        # get users from list

        # event = Event.create(
        #     title=command.title,
        #     description=command.description,
        #     status=command.status,
        #     created_at = command.created_at,
        #     updated_at = command.updated_at,
        #     startTime = command.startTime,
        #     endTime = command.endTime
        # )
        eventDTO = EventDTOCreate(
            title=command.title,
            description=command.description,
            status=command.status,
            created_at = command.created_at,
            updated_at = command.updated_at,
            startTime = command.startTime,
            endTime = command.endTime,
            invitees = command.invitees
        )

        return await self.event_repository.create_event(eventDTO)

    # def get_event_by_id(self, id: int) -> Event:
    #     return self.event_repository.get_event_by_id(id)
    async def get_event_by_id(self, id: int) -> EventDTO | Exception:
        eventDTO = await self.event_repository.get_event_by_id(id)
        if eventDTO is None:
            raise HTTPException(status_code=404, detail="Event not found")

        return eventDTO
        # invitees = [str(user_id) for user_id in event_data.invitees] if event_data.invitees else []
        # invitees = []
        # return EventDTO(
        #     id=event_data.id,
        #     title=event_data.title,
        #     description=event_data.description,
        #     status=event_data.status,
        #     startTime=event_data.startTime,
        #     endTime=event_data.endTime,
        #     invitees=invitees,
        #     created_at=event_data.created_at,
        #     updated_at=event_data.updated_at
        # )

    @Transactional()
    async def delete_event_by_id(self, event_id: int) -> bool:
        return await self.event_repository.delete_event_by_id(event_id)

    async def merge_all_overlapping_events(self, user_id: int) -> List[EventDTO]:
        return await self.event_repository.merge_all_overlapping_events(user_id)

