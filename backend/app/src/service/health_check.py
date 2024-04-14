from sqlalchemy import text
from sqlalchemy.orm import Session


class HealthCheckService:
    def __init__(self, session: Session):
        self.__session = session

    def check_health(self) -> bool:
        try:
            self.__session.execute(statement=text("""SELECT 1"""))
        except Exception as ex:
            return False
        return True
