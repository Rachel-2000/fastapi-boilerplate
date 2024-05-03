from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.event.adapter.output.persistence.repository_adapter import EventRepositoryAdapter
from app.event.adapter.output.persistence.sqlalchemy.event_repository_impl import EventSQLAlchemyRepo
from app.event.application.service.event_service import EventService


class EventContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    # Repository for Events using SQLAlchemy as the ORM
    event_sqlalchemy_repo = Singleton(EventSQLAlchemyRepo)

    # Adapter that implements a higher level repository interface
    event_repository_adapter = Factory(
        EventRepositoryAdapter,
        repository=event_sqlalchemy_repo,
    )

    # Service that uses the repository adapter
    event_service = Factory(EventService, repository=event_repository_adapter)
