from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from app.event.application.service.event_service import EventService
from app.container import Container
from app.event.adapter.input.api.v1.request import CreateEventRequest, RetrieveEventRequest, DeleteEventRequest
from app.event.application.dto import EventDTO
from app.event.domain.command import CreateEventCommand
from app.event.domain.usecase.event import EventUseCase
from typing import List
from datetime import datetime


event_router = APIRouter()

# @event_router.post("/", response_model=EventDTO)
@event_router.post("/", response_model=bool)
@inject
async def create_event(
        request: CreateEventRequest,
        usecase: EventUseCase = Depends(Provide[Container.event_service])):
    command = CreateEventCommand(**request.model_dump())
    return await usecase.create_event(command=command)


@event_router.get("/{event_id}", response_model=EventDTO)
@inject
async def get_event(
        event_id: int,
        usecase: EventUseCase = Depends(Provide[Container.event_service])):
    return await usecase.get_event_by_id(id=event_id)


@event_router.delete("/{event_id}", response_model=bool)
@inject
async def delete_event(
        event_id: int,
        usecase: EventUseCase = Depends(Provide[Container.event_service])):

    return await usecase.delete_event_by_id(event_id=event_id)


@event_router.put("/merge-all/{uid}", response_model=List[EventDTO])
@inject
async def update_event(
        uid: int,
        usecase: EventUseCase = Depends(Provide[Container.event_service])):

    return await usecase.merge_all_overlapping_events(user_id=uid)
