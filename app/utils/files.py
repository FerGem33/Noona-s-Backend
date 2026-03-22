from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import settings


def ensure_upload_directories() -> None:
    base_dir = Path(settings.UPLOAD_DIR)
    (base_dir / "productos").mkdir(parents=True, exist_ok=True)
    (base_dir / "materia_prima").mkdir(parents=True, exist_ok=True)


def validate_image_content_type(content_type: str | None) -> None:
    if content_type not in settings.ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no permitido. Solo se aceptan JPEG, PNG y WEBP"
        )


def generate_unique_filename() -> str:
    return f"{uuid4().hex}.webp"


def get_absolute_path(relative_path: str) -> Path:
    return Path(settings.UPLOAD_DIR) / relative_path


def build_image_url(relative_path: str | None) -> str | None:
    if not relative_path:
        return None

    return f"{settings.MEDIA_URL_PREFIX}/{relative_path}"


def delete_file_if_exists(relative_path: str | None) -> None:
    if not relative_path:
        return

    absolute_path = get_absolute_path(relative_path)

    try:
        if absolute_path.exists() and absolute_path.is_file():
            absolute_path.unlink()
    except OSError:
        pass


async def save_image_file(upload_file: UploadFile, entity_folder: str) -> str:
    validate_image_content_type(upload_file.content_type)

    file_bytes = await upload_file.read()

    if len(file_bytes) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La imagen excede el tamano maximo permitido de {settings.MAX_IMAGE_SIZE // (1024 * 1024)} MB"
        )

    try:
        image = Image.open(BytesIO(file_bytes))
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo no es una imagen valida"
        )

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

    filename = generate_unique_filename()
    relative_path = f"{entity_folder}/{filename}"
    absolute_path = get_absolute_path(relative_path)

    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    if image.mode == "RGBA":
        image.save(
            absolute_path,
            format="WEBP",
            quality=80,
            method=6
        )
    else:
        image = image.convert("RGB")
        image.save(
            absolute_path,
            format="WEBP",
            quality=80,
            method=6
        )

    await upload_file.close()
    return relative_path