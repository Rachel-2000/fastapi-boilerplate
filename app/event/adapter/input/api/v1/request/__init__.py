from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CreateEventRequest(BaseModel):
    title: str
    description: str = None
    status: str = "TODO" # default value: TODO
    startTime: datetime = Field(default_factory=datetime.now)
    endTime: datetime = Field(default_factory=datetime.now)
    invitees: Optional[List[str]] = [] # list of user ids


class RetrieveEventRequest(BaseModel):
    id: int

class DeleteEventRequest(BaseModel):
    id: int




# class CreateEventRequest(BaseModel):
#     title: str = Field(..., description="Event Title")
#     description: str = Field(None, description="Description of the event")
#     status: str = Field(..., description="Event Status (TODO, IN_PROGRESS, COMPLETED)")
#     startTime: datetime = Field(..., description="Start time of the event")
#     endTime: datetime = Field(..., description="End time of the event")
#     invitees: List[str] = Field(..., description="List of user IDs to invite to the event")
#
# class MergeEventsRequest(BaseModel):
#     user_id: int = Field(..., description="ID of the user to merge events for")


