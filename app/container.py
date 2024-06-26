from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.auth.application.service.jwt import JwtService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService
from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.adapter.output.persistence.sqlalchemy.event_repository_impl import EventSQLAlchemyRepo
from app.event.application.service.event_service import EventService


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    user_repo = Singleton(UserSQLAlchemyRepo)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    user_service = Factory(UserService, repository=user_repo_adapter)

    event_repo = Singleton(EventSQLAlchemyRepo)
    event_repo_adapter = Factory(EventRepositoryAdapter, event_repo=event_repo)
    event_service = Factory(EventService, repository=event_repo_adapter)

    jwt_service = Factory(JwtService)
