from dependency_injector import containers, providers
from src.infrastructure.database.database_session_manager import DatabaseSessionManager
from src.infrastructure.repository.video import VideoRepository
from src.service.file import FileService
from src.service.health_check import HealthCheckService
from src.service.video import VideoService


def session_factory(conn_string: str):
    database_session_manager = DatabaseSessionManager(conn_string=conn_string)
    with database_session_manager.session() as session:
        yield session


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session = providers.Resource(session_factory, conn_string=config.database_url)


class RepositoryContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    video_repository = providers.Factory(
        VideoRepository, session=infrastructure.session
    )


class ServiceContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    repository = providers.DependenciesContainer()

    health_check_service = providers.Factory(
        HealthCheckService, session=infrastructure.session
    )

    file_service = providers.Factory(FileService)

    video_service = providers.Factory(
        VideoService,
        video_repository=repository.video_repository,
    )


class AppContainer(containers.DeclarativeContainer):
    config = Core.config

    infrastructure = providers.Container(InfrastructureContainer, config=config)

    repository = providers.Container(RepositoryContainer, infrastructure=infrastructure)

    service = providers.Container(
        ServiceContainer, infrastructure=infrastructure, repository=repository
    )
