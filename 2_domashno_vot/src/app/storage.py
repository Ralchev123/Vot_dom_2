# src/app/storage.py
from minio import Minio
from minio.error import S3Error
import uuid
from fastapi import UploadFile
from .config import Settings

class MinioStorage:
    def __init__(self, settings: Settings):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False
        )
        self.bucket_name = "files"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    async def upload_file(self, file: UploadFile, user_id: str) -> str:
        file_id = str(uuid.uuid4())
        metadata = {
            "user_id": user_id,
            "original_filename": file.filename
        }
        
        try:
            file_data = await file.read()
            self.client.put_object(
                self.bucket_name,
                file_id,
                file_data,
                len(file_data),
                metadata=metadata
            )
            return file_id
        finally:
            await file.close()

    async def download_file(self, file_id: str, user_id: str):
        try:
            obj = self.client.get_object(self.bucket_name, file_id)
            metadata = obj.stats().metadata
            if metadata.get("user_id") != user_id:
                raise PermissionError("Access denied")
            return obj
        except S3Error as e:
            raise FileNotFoundError(f"File not found: {file_id}")

    async def update_file(self, file_id: str, new_file: UploadFile, user_id: str) -> str:
        try:
            # Check if file exists and user has permission
            obj = self.client.get_object(self.bucket_name, file_id)
            metadata = obj.stats().metadata
            if metadata.get("user_id") != user_id:
                raise PermissionError("Access denied")
            
            # Upload new version
            await self.delete_file(file_id, user_id)
            return await self.upload_file(new_file, user_id)
        except S3Error:
            raise FileNotFoundError(f"File not found: {file_id}")

    async def delete_file(self, file_id: str, user_id: str):
        try:
            # Check if user has permission
            obj = self.client.get_object(self.bucket_name, file_id)
            metadata = obj.stats().metadata
            if metadata.get("user_id") != user_id:
                raise PermissionError("Access denied")
            
            self.client.remove_object(self.bucket_name, file_id)
        except S3Error:
            raise FileNotFoundError(f"File not found: {file_id}")