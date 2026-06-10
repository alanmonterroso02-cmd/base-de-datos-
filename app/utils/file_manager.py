import os
import shutil
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status

from app.core.settings import BASE_DIR

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}
ALLOWED_IMAGE_MIMES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
    "image/bmp",
    "image/svg+xml",
}

UPLOAD_DIR = BASE_DIR / "app" / "static" / "uploads"


class FileManager:
    @classmethod
    def validate_image(cls, upload_file: UploadFile) -> None:
        ext = os.path.splitext(upload_file.filename)[1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato de imagen no válido: {ext}. Permitidos: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}",
            )
        content_type = upload_file.content_type
        if content_type and content_type not in ALLOWED_IMAGE_MIMES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo MIME no válido: {content_type}",
            )

    @classmethod
    def save_upload_file(cls, upload_file: UploadFile, subdir: str = "premios") -> str:
        cls.validate_image(upload_file)
        upload_dir = UPLOAD_DIR / subdir
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_extension = os.path.splitext(upload_file.filename)[1].lower()
        filename = f"{uuid4()}{file_extension}"
        file_path = upload_dir / filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        return f"/static/uploads/{subdir}/{filename}"

    @classmethod
    def delete_file(cls, public_url: str) -> bool:
        if not public_url:
            return False
        relative = public_url.lstrip("/")
        file_path = BASE_DIR / "app" / relative
        try:
            if file_path.exists():
                file_path.unlink()
                return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
        return False
