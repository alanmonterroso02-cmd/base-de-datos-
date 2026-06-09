import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}
ALLOWED_IMAGE_MIMES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
    "image/bmp",
    "image/svg+xml",
}

class FileManager:

    UPLOAD_BASE = "static/uploads"

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
        """Saves an uploaded file and returns the public URL."""
        cls.validate_image(upload_file)
        upload_dir = os.path.join(cls.UPLOAD_BASE, subdir)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_extension = os.path.splitext(upload_file.filename)[1].lower()
        filename = f"{uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        return f"/static/uploads/{subdir}/{filename}"

    @classmethod
    def delete_file(cls, public_url: str) -> bool:
        """Deletes a file from the server given its public URL."""
        if not public_url:
            return False

        # Convert public URL to system path: /static/... -> static/...
        file_path = public_url.replace("/static", "static")

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

        return False
