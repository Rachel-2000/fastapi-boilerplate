from abc import ABC, abstractmethod
from typing import List

from app.event.application.dto import EventDTO
from app.event.domain.entity.event import Event
from app.event.domain.command import CreateEventCommand

class EventUseCase(ABC):
    @abstractmethod
    async def get_event_by_id(self, *, id: int) -> Event:
        """Get event list"""

    @abstractmethod
    # async def create_event(self, *, command: CreateEventCommand) -> Event:
    async def create_event(self, *, command: CreateEventCommand) -> bool:
        """Create Event"""

    @abstractmethod
    async def merge_all_overlapping_events(self, *, user_id: int) -> List[EventDTO]:
        """Merge overlapping events"""

    @abstractmethod
    async def delete_event_by_id(self, *, event_id: int) -> bool:
        """Delete event"""
