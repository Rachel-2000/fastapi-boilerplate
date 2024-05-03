from sqlalchemy import select

from app.event.application.dto import EventDTO, EventDTOCreate
from app.event.domain.entity.event import Event, event_user_association_table
from app.event.domain.repository.event_repository import EventRepository
from app.user.domain.entity.user import User
from core.db.session import session_factory
from core.db import Transactional
from typing import List, Optional


class EventSQLAlchemyRepo(EventRepository):
    # async def create_event(self, event: Event) -> Event:
    #     async with session_factory() as write_session:
    #         write_session.add(event)
    #         # write_session.commit()
    #         # write_session.refresh(event)
    #     return event
    async def create_event(self, eventDTO: EventDTOCreate) -> bool:
        # select users from invitees list
        invitees = [int(user_id_str) for user_id_str in eventDTO.invitees]
        async with session_factory() as read_session:
            stmt = await read_session.execute(select(User).where(User.id.in_(invitees)))
            users_list = stmt.scalars().all()

        event = Event.create(
            title=eventDTO.title,
            description=eventDTO.description,
            status=eventDTO.status,
            created_at = eventDTO.created_at,
            updated_at = eventDTO.updated_at,
            startTime = eventDTO.startTime,
            endTime = eventDTO.endTime,
            invitees = users_list
        )

        async with session_factory() as write_session:
            try:
                write_session.add(event)
                await write_session.commit()
                await write_session.refresh(event)
                return True
            except Exception as e:
                await write_session.rollback()
                print(f"Failed to add event: {e}")
                return False

    async def get_event_by_id(self, event_id: int) -> EventDTO | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(select(Event).where(Event.id == event_id))
            event_data = stmt.scalars().first()
            await read_session.refresh(event_data, ["invitees"])
            invitees = [str(user.id) for user in event_data.invitees]

        return EventDTO(
            id=event_data.id,
            title=event_data.title,
            description=event_data.description,
            status=event_data.status,
            startTime=event_data.startTime,
            endTime=event_data.endTime,
            invitees=invitees,
            created_at=event_data.created_at,
            updated_at=event_data.updated_at
        )

    # @Transactional()
    async def delete_event_by_id(self, event_id: int) -> bool:
        async with session_factory() as read_session:
            stmt = await read_session.execute(select(Event).where(Event.id == event_id))
            event = stmt.scalars().first()

        async with session_factory() as write_session:
            # event = await self.get_event_by_id(event_id)
            if event:
                await write_session.delete(event)
                await write_session.commit()
                return True
            return False


    async def merge_all_overlapping_events(self, user_id: int) -> List[EventDTO]:
        async with session_factory() as write_session:
            # collect all events belonging to the user
            stmt = await write_session.execute(select(Event).join(event_user_association_table).where(
                event_user_association_table.c.user_id == user_id))
            events = stmt.scalars().all()
            event_ids = [event.id for event in events]

        merged_events = []
        event_lists = []
        for id in event_ids:
            eventDTO = await self.get_event_by_id(id)
            event_lists.append(eventDTO)

        # dictionary to store merged events
        merged_events_dict = {}

        # merge overlapping events
        for event in event_lists:
            merged = False
            for merged_event in merged_events_dict.values():
                if event.startTime < merged_event.endTime or event.endTime > merged_event.startTime:
                    # overlapping events found, merge them
                    merged_event.startTime = min(event.startTime, merged_event.startTime)
                    merged_event.endTime = max(event.endTime, merged_event.endTime)
                    # concatenate titles and descriptions
                    merged_event.title += f" + {event.title}"
                    merged_event.description += f" ; {event.description}"

                    # invite all members from each merged event
                    merged_event.invitees = list(set(merged_event.invitees).union(set(event.invitees)))
                    # choose status
                    if event.status == "COMPLETED" or merged_event.status == "COMPLETED":
                        merged_event.status = "COMPLETED"
                    elif event.status == "IN_PROGRESS" or merged_event.status == "IN_PROGRESS":
                        merged_event.status = "IN_PROGRESS"
                    else:
                        merged_event.status = "TODO"
                    merged = True
                    break
            if not merged:
                # unmerged single event
                merged_events_dict[event.id] = event

        # invite all members from each merged event
        # for merged_event in merged_events_dict.values():
        #     for user in merged_event.invitees:
        #         merged_event.invitees.extend(user.invitees)

        # delete the original overlapping events
        for id in event_ids:
            await self.delete_event_by_id(id)

        return list(merged_events_dict.values())
        # create new merged event


        # return [EventDTO(
        #         id=event.id,
        #         title=event.title,
        #         description=event.description,
        #         status=event.status,
        #         startTime=event.startTime,
        #         endTime=event.endTime,
        #         invitees=[invitee.id for invitee in event.invitees],
        #         created_at=event.created_at,
        #         updated_at=event.updated_at
        #     ) for event in merged_events]


    # async def merge_all_overlapping_events(self, user_id: int) -> List[EventDTO]:
    #     async with session_factory() as write_session:
    #         # collect all events belonging to the user
    #         stmt = await write_session.execute(select(Event).join(event_user_association_table).where(
    #             event_user_association_table.c.user_id == user_id))
    #         events = stmt.scalars().all()
    #
    #         merged_events = []
    #
    #         # dictionary to store merged events
    #         merged_events_dict = {}
    #
    #         # merge overlapping events
    #         for event in events:
    #             merged = False
    #             for merged_event in merged_events_dict.values():
    #                 if event.startTime < merged_event.endTime or event.endTime > merged_event.startTime:
    #                     # overlapping events found, merge them
    #                     merged_event.startTime = min(event.startTime, merged_event.startTime)
    #                     merged_event.endTime = max(event.endTime, merged_event.endTime)
    #                     # concatenate titles and descriptions
    #                     merged_event.title += f" + {event.title}"
    #                     merged_event.description += f" ; {event.description}"
    #
    #                     # choose status
    #                     if event.status == "COMPLETED" or merged_event.status == "COMPLETED":
    #                         merged_event.status = "COMPLETED"
    #                     elif event.status == "IN_PROGRESS" or merged_event.status == "IN_PROGRESS":
    #                         merged_event.status = "IN_PROGRESS"
    #                     else:
    #                         merged_event.status = "TODO"
    #                     merged = True
    #                     break
    #             if not merged:
    #                 # unmerged single event
    #                 merged_events_dict[event.id] = event
    #         # invite all members from each merged event
    #         # for merged_event in merged_events_dict.values():
    #         #     for user in merged_event.invitees:
    #         #         merged_event.invitees.extend(user.invitees)
    #         for merged_event in merged_events_dict.values():
    #             extended_invitees = []
    #             for user in merged_event.invitees:
    #                 extended_invitees.extend(user.invitees)
    #             merged_event.invitees = extended_invitees
    #     return []
    #         # delete the original overlapping events
    #         # event_ids_to_delete = [event_id for merged_event in merged_events_dict.values() for event_id in
    #         #                        merged_event.original_event_ids]
    #         # events_to_delete = await write_session.execute(select(Event).where(Event.id.in_(event_ids_to_delete)))
    #         # for event_to_delete in events_to_delete.scalars().all():
    #         #     await write_session.delete(event_to_delete)
    #         #
    #         # merged_events.extend(merged_events_dict.values())
    #
    #
    #     # return [EventDTO(
    #     #         id=event.id,
    #     #         title=event.title,
    #     #         description=event.description,
    #     #         status=event.status,
    #     #         startTime=event.startTime,
    #     #         endTime=event.endTime,
    #     #         invitees=[invitee.id for invitee in event.invitees],
    #     #         created_at=event.created_at,
    #     #         updated_at=event.updated_at
    #     #     ) for event in merged_events]

    # async def merge_all_overlapping_events(self, user_id: int) -> List[EventDTO]:
    #     async with session_factory() as write_session:
    #         # collect all events belonging to the user
    #         stmt = await write_session.execute(select(Event).join(event_user_association_table).where(
    #             event_user_association_table.c.user_id == user_id))
    #         events = stmt.scalars().all()
    #
    #         merged_events = []
    #
    #         # dictionary to store merged events
    #         merged_events_dict = {}
    #
    #         # merge overlapping events
    #         for event in events:
    #             merged = False
    #             for merged_event in merged_events_dict.values():
    #                 if event.startTime < merged_event.endTime and event.endTime > merged_event.startTime:
    #                     # Overlapping events found, merge them
    #                     merged_event.startTime = min(event.startTime, merged_event.startTime)
    #                     merged_event.endTime = max(event.endTime, merged_event.endTime)
    #                     # Concatenate titles and descriptions
    #                     merged_event.title += f" + {event.title}"
    #                     merged_event.description += f" ; {event.description}"
    #                     # Choose a reasonable value for status
    #                     if event.status == "COMPLETED" or merged_event.status == "COMPLETED":
    #                         merged_event.status = "COMPLETED"
    #                     elif event.status == "IN_PROGRESS" or merged_event.status == "IN_PROGRESS":
    #                         merged_event.status = "IN_PROGRESS"
    #                     else:
    #                         merged_event.status = "TODO"
    #                     merged = True
    #                     break
    #             if not merged:
    #                 # If no overlapping events, add event as a new merged event
    #                 merged_events_dict[event.id] = event
    #
    #             # Invite all members from each merged event
    #         for merged_event in merged_events_dict.values():
    #             for user in merged_event.invitees:
    #                 merged_event.invitees.extend(user.invitees)
    #
    #             # Delete the original overlapping events
    #             for event_id in merged_event.original_event_ids:
    #                 event_to_delete = await write_session.get(Event, event_id)
    #                 if event_to_delete:
    #                     write_session.delete(event_to_delete)
    #
    #             merged_events.append(merged_event)
    #
    #         return [EventDTO(
    #             id=event.id,
    #             title=event.title,
    #             description=event.description,
    #             status=event.status,
    #             startTime=event.startTime,
    #             endTime=event.endTime,
    #             invitees=[invitee.id for invitee in event.invitees],
    #             created_at=event.created_at,
    #             updated_at=event.updated_at
    #         ) for event in merged_events]


