from sqlalchemy import text
from sqlalchemy.orm import Session
from src.utils.api_exceptions import ServerErrorException


class HealthCheckService:
    def __init__(self, session: Session):
        self.session = session

    def check_health(self) -> bool:
        try:
            self.session.execute(statement=text("""SELECT 1"""))
        except Exception as ex:
            raise ServerErrorException(
                extra=f"The application isn't ready to work as expected: {str(ex)}"
            )

        return True
