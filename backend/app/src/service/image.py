from src.infrastructure import application_settings
from src.utils.api_exceptions import BadRequestException, ServerErrorException
from src.utils.file_extension import is_allowed_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class ImageService:
    def save_image(self, file: FileStorage) -> str:
        if file.filename == "":
            raise BadRequestException(extra="No selected file")

        if not is_allowed_file(filename=file.filename):
            raise BadRequestException(
                extra=f"File extension of file={file.filename} not allowed"
            )

        filename = secure_filename(file.filename)

        path = self.__create_path(filename=filename)

        try:
            file.save(path)
        except Exception as ex:
            raise ServerErrorException(extra=f"File={filename} not saved")

        return path

    @staticmethod
    def __create_path(filename: str) -> str:
        return "".join(["/", "app", application_settings.upload_folder, "/", filename])
