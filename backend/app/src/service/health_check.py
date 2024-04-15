from sqlalchemy import text
from sqlalchemy.orm import Session
from src.utils.api_exceptions import ServerErrorException


class HealthCheckService:
    def __init__(self, session: Session):
        self.__session = session

    def check_health(self) -> bool:
        try:
            self.__session.execute(statement=text("""SELECT 1"""))
        except Exception as ex:
            raise ServerErrorException(
                extra="The application isn't ready to work as expected"
            )

        return True
