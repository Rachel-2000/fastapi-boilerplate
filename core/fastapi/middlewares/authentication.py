import jwt
from pydantic import BaseModel, Field
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from typing import List, Optional

from core.config import config


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
    name: str = Field(None, description="Username")
    events: List[str] = Field(default_factory=list, description="Events")

# Example usage:
# user = CurrentUser(id=123, name="Rachel", events=["event1", "event2"])

class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[bool, CurrentUser | None]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not credentials:
            return False, current_user

        try:
            payload = jwt.decode(
                credentials,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            user_id = payload.get("user_id")
            user_events = payload.get("user_events", [])  
            # Extract events list, defaulting to empty if not present
            user_name = payload.get("user_name")
        except jwt.exceptions.PyJWTError:
            return False, current_user

        current_user.id = user_id
        current_user.name = user_name
        current_user.events = user_events
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
