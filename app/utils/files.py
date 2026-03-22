from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from app.core.config import settings


def ensure_upload_directories() -> None:
    base_dir = Path(settings.UPLOAD_DIR)
    (base_dir / "productos").mkdir(parents=True, exist_ok=True)
    (base_dir / "materia_prima").mkdir(parents=True, exist_ok=True)


def validate_image_content_type(content_type: str | None) -> str:
    if content_type not in settings.ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no permitido. Solo se aceptan JPEG, PNG y WEBP"
        )

    return settings.ALLOWED_IMAGE_MIME_TYPES[content_type]


async def validate_image_size(upload_file: UploadFile) -> None:
    current_position = upload_file.file.tell()
    upload_file.file.seek(0, 2)
    file_size = upload_file.file.tell()
    upload_file.file.seek(current_position)

    if file_size > settings.MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La imagen excede el tamaño maximo permitido de {settings.MAX_IMAGE_SIZE // (1024 * 1024)} MB"
        )


def generate_unique_filename(extension: str) -> str:
    return f"{uuid4().hex}{extension}"


def get_absolute_path(relative_path: str) -> Path:
    return Path(settings.UPLOAD_DIR) / relative_path


def build_image_url(relative_path: str | None) -> str | None:
    if not relative_path:
        return None

    return f"{settings.MEDIA_URL_PREFIX}/{relative_path}"


async def save_image_file(upload_file: UploadFile, entity_folder: str) -> str:
    extension = validate_image_content_type(upload_file.content_type)
    await validate_image_size(upload_file)

    filename = generate_unique_filename(extension)
    relative_path = f"{entity_folder}/{filename}"
    absolute_path = get_absolute_path(relative_path)

    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    with absolute_path.open("wb") as output_file:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            output_file.write(chunk)

    await upload_file.close()
    return relative_path


def delete_file_if_exists(relative_path: str | None) -> None:
    if not relative_path:
        return

    absolute_path = get_absolute_path(relative_path)

    try:
        if absolute_path.exists() and absolute_path.is_file():
            absolute_path.unlink()
    except OSError:
        pass