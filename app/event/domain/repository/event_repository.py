from abc import ABC, abstractmethod
from typing import List

from app.event.application.dto import EventDTO, EventDTOCreate
from app.event.domain.entity.event import Event

class EventRepository(ABC):
    @abstractmethod
    async def get_event_by_id(self, id: int) -> EventDTO:
        """Get event by id"""

    @abstractmethod
    # async def create_event(self, event: Event) -> Event:
    async def create_event(self, eventDTO: EventDTOCreate) -> bool:
        """Create an event"""

    @abstractmethod
    async def delete_event_by_id(self, id: int) -> bool:
        """Delete event by id"""

    @abstractmethod
    async def merge_all_overlapping_events(self, user_id: int) -> List[EventDTO]:
        """Merge all events belongs to the user id"""

# class UserRepo(ABC):
#     @abstractmethod
#     async def get_users(
#         self,
#         *,
#         limit: int = 12,
#         prev: int | None = None,
#     ) -> list[User]:
#         """Get user list"""
#
#     @abstractmethod
#     async def get_user_by_email_or_nickname(
#         self,
#         *,
#         email: str,
#         nickname: str,
#     ) -> User | None:
#         """Get user by email or nickname"""
#
#     @abstractmethod
#     async def get_user_by_id(self, *, user_id: int) -> User | None:
#         """Get user by id"""
#
#     @abstractmethod
#     async def get_user_by_email_and_password(
#         self,
#         *,
#         email: str,
#         password: str,
#     ) -> User | None:
#         """Get user by email and password"""
#
#     @abstractmethod
#     async def save(self, *, user: User) -> None:
#         """Save user"""
