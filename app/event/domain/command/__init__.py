from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class CreateEventCommand(BaseModel):
    # id: int
    title: str
    description: str | None = None
    status: str
    startTime: datetime
    endTime: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    invitees: List[str] | None = []