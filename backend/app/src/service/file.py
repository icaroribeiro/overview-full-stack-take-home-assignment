import os

from src.infrastructure import application_settings
from src.utils.api_exceptions import BadRequestException, ServerErrorException
from src.utils.file_extension import is_allowed_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class FileService:
    @staticmethod
    def save_file(file: FileStorage, allowed_extensions: list[str]) -> str:
        if file.filename == "":
            raise BadRequestException(extra="No selected file")

        if not is_allowed_file(
            filename=file.filename, allowed_extensions=allowed_extensions
        ):
            raise BadRequestException(
                extra=f"File extension of file={file.filename} is not allowed"
            )

        filename = secure_filename(file.filename)

        path = os.path.join(application_settings.upload_folder, filename)

        try:
            file.save(path)
        except Exception as ex:
            raise ServerErrorException(
                extra=f"Failed to save file={filename}: {str(ex)}"
            )

        return path
