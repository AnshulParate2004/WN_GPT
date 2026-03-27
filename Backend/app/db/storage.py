"""
Supabase Storage Manager
────────────────────────
Handles file uploads to Supabase buckets (PDFs, Images, Medical Reports).
"""
from __future__ import annotations
import uuid
from app.db.supabase import get_supabase
from app.core.config import get_settings

settings = get_settings()


class StorageManager:
    @staticmethod
    async def upload_file(
        file_bytes: bytes,
        file_name: str,
        content_type: str,
        bucket: str = "patient-docs"
    ) -> dict:
        """Uploads a file to a Supabase bucket and returns the metadata + URL."""
        supabase = get_supabase()
        
        # Unique path: patient_id/uuid_filename
        ext = file_name.split(".")[-1] if "." in file_name else "bin"
        storage_path = f"uploads/{uuid.uuid4()}.{ext}"

        # Upload to bucket
        # Note: Supabase Python client's storage.upload is synchronous for now
        res = supabase.storage.from_(bucket).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type}
        )
        
        # Get public URL
        public_url = supabase.storage.from_(bucket).get_public_url(storage_path)

        return {
            "bucket": bucket,
            "path": storage_path,
            "url": public_url,
            "file_name": file_name,
            "file_type": content_type
        }


storage_manager = StorageManager()
