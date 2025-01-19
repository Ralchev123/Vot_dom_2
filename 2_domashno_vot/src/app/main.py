# src/app/main.py
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .auth import verify_token
from .storage import MinioStorage
from .config import Settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="File Management System")
settings = Settings()
storage = MinioStorage(settings)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = verify_token(token)
        file_id = await storage.upload_file(file, user["sub"])
        logger.info(f"File uploaded successfully: {file_id}")
        return {"file_id": file_id}
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_id}")
async def download_file(
    file_id: str,
    token: str = Depends(oauth2_scheme)
):
    try:
        user = verify_token(token)
        file_data = await storage.download_file(file_id, user["sub"])
        logger.info(f"File downloaded successfully: {file_id}")
        return file_data
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/update/{file_id}")
async def update_file(
    file_id: str,
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme)
):
    try:
        user = verify_token(token)
        updated_id = await storage.update_file(file_id, file, user["sub"])
        logger.info(f"File updated successfully: {file_id}")
        return {"file_id": updated_id}
    except Exception as e:
        logger.error(f"Update failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/{file_id}")
async def delete_file(
    file_id: str,
    token: str = Depends(oauth2_scheme)
):
    try:
        user = verify_token(token)
        await storage.delete_file(file_id, user["sub"])
        logger.info(f"File deleted successfully: {file_id}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Delete failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))