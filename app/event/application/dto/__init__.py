from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from typing import List, Optional

class EventDTOBase(BaseModel):
    title: str
    description: Optional[str]
    status: str
    startTime: datetime
    endTime: datetime
    invitees: Optional[List[str]] # List of UserIDs in str

class EventDTOCreate(EventDTOBase):
    created_at: datetime
    updated_at: datetime

class EventDTOUpdate(EventDTOBase):
    pass

class EventDTO(EventDTOBase):
    id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

