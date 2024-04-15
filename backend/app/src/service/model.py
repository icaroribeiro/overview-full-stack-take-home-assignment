from typing import Optional

from src.utils.model import Model


class ModelService:
    def __init__(self):
        self.__model = None

    def set_model(self, name: str) -> Model:
        try:
            self.__model = Model(model_name=name)
        except Exception as ex:
            raise ex

        return self.__model

    def get_model(self) -> Optional[Model]:
        return self.__model
