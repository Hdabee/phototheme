from pathlib import Path

from fastapi import HTTPException, UploadFile

DATA_DIR = Path("data")
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUTS_DIR = DATA_DIR / "outputs"
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


def ensure_storage_directories() -> None:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


async def safe_image_upload(upload: UploadFile, target_base: Path) -> Path:
    if upload.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formats acceptes : JPEG, PNG, WEBP.",
        )

    suffix = Path(upload.filename or "photo.jpg").suffix.lower() or ".jpg"
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        suffix = ".jpg"

    content = await upload.read()
    if not content:
        raise HTTPException(status_code=400, detail="Le fichier est vide.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Le fichier depasse la limite de 10 MB.",
        )

    destination = target_base.with_suffix(suffix)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return destination
