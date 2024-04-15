from src.infrastructure import application_settings


def is_allowed_file(filename: str, allowed_extensions: list[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions
