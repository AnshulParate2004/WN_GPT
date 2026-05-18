"""
Local Storage Manager
────────────────────────
Handles file uploads to the local `uploads/` directory.
"""
from __future__ import annotations
import os
import uuid
from pathlib import Path

class StorageManager:
    @staticmethod
    async def upload_file(
        file_bytes: bytes,
        file_name: str,
        content_type: str,
        bucket: str = "patient-docs"
    ) -> dict:
        """Uploads a file locally and returns the metadata + URL."""
        # We will ignore 'bucket' and put everything in 'uploads'
        ext = file_name.split(".")[-1] if "." in file_name else "bin"
        unique_name = f"{uuid.uuid4()}.{ext}"
        
        base_dir = Path(__file__).resolve().parents[2]
        uploads_dir = base_dir / "uploads"
        uploads_dir.mkdir(exist_ok=True)
        
        file_path = uploads_dir / unique_name
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        # The public URL will be served via FastAPI static files
        public_url = f"/uploads/{unique_name}"

        return {
            "bucket": "local-uploads",
            "path": unique_name,
            "url": public_url,
            "file_name": file_name,
            "file_type": content_type
        }

storage_manager = StorageManager()
