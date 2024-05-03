from app.event.application.dto import EventDTO, EventDTOCreate
from app.event.domain.entity.event import Event
from app.event.domain.repository.event_repository import EventRepository


class EventRepositoryAdapter:
    def __init__(self, *, event_repo: EventRepository):
        self.event_repo = event_repo

    # async def create_event(self, event: Event) -> Event:
    async def create_event(self, eventDTO: EventDTOCreate) -> bool:
        return await self.event_repo.create_event(eventDTO=eventDTO)

    async def get_event_by_id(self, event_id: int) -> EventDTO | None:
        return await self.event_repo.get_event_by_id(event_id=event_id)

    async def delete_event_by_id(self, event_id: int) -> bool:
        return await self.event_repo.delete_event_by_id(event_id=event_id)

    async def merge_all_overlapping_events(self, user_id: int) -> EventDTO:
        return await self.event_repo.merge_all_overlapping_events(user_id=user_id)

# from typing import List, Optional
# from app.event.domain.entity.event import Event
# from app.event.domain.repository.event_repository import EventRepository
#
# class EventRepositoryAdapter:
#     def __init__(self, *, event_repo: EventRepository):
#         self.event_repo = event_repo
#
#     async def create_event(self, event: Event) -> Event:
#         created_event = await self.event_repo.create_event(event)
#         return EventRead.model_validate(created_event)
#
#     async def get_event_by_id(self, event_id: int) -> Optional[EventRead]:
#         event = await self.event_repo.get_event_by_id(event_id)
#         if event:
#             return EventRead.model_validate(event)
#         return None
#
#     async def delete_event_by_id(self, event_id: int) -> bool:
#         return await self.event_repo.delete_event_by_id(event_id)
#
#     async def merge_all_overlapping_events(self, user_id: int) -> List[EventRead]:
#         events = await self.event_repo.merge_all_overlapping_events(user_id)
#         return [EventRead.model_validate(event) for event in events]


