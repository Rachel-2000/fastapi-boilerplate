from pydantic import BaseModel, Field
from typing import List
# from app.event.application.dto import EventDTO
#
# class UserDTO(BaseModel):
#     id: int = Field(..., description="ID")
#     name: str = Field(..., description="Username")
#     events: List[EventDTO] = Field(..., description="Eventlist")

class GetUserListResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class CreateUserRequestDTO(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    nickname: str = Field(..., description="Nickname")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class LoginResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
