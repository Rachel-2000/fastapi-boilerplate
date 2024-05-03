from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class EventResponse(BaseModel):
    id: int = Field(..., description="Event ID")
    title: str = Field(..., description="Event Title")
    description: str = Field(None, description="Description of the event")
    status: str = Field(..., description="Event Status (TODO, IN_PROGRESS, COMPLETED)")
    created_at: datetime = Field(..., description="Created Date")
    updated_at: datetime = Field(..., description="Last Updated Date")
    startTime: datetime = Field(..., description="Start time of the event")
    endTime: datetime = Field(..., description="End time of the event")
    invitees: Optional[List[str]] = Field(..., description="List of user IDs invited to the event")

