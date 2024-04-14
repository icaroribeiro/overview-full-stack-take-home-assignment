from dependency_injector import containers, providers
from src.infrastructure.database.database_session_manager import DatabaseSessionManager
from src.service.health_check import HealthCheckService


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


class ServiceContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    health_check_service = providers.Factory(
        HealthCheckService, session=infrastructure.session
    )


class AppContainer(containers.DeclarativeContainer):
    config = Core.config

    infrastructure = providers.Container(InfrastructureContainer, config=config)

    service = providers.Container(ServiceContainer, infrastructure=infrastructure)
