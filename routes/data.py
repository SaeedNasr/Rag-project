from fastapi import Depends, FastAPI, APIRouter ,UploadFile,status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings,Settings
from controllers import DataController
from controllers.ProjectController import ProjectController
import aiofiles
from models import ResponseSignal
import logging 
loger = logging.getLogger("uvicorn.error")
data_router = APIRouter(prefix="/api/v1/data",
                         tags=["api_v1",["data"]])

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    datacontroller = DataController()
    is_valid ,result_signal= datacontroller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message":result_signal.value})
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = datacontroller.generate_unique_file_name(original_filename=file.filename,
                                                  project_id=project_id)
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"message":ResponseSignal.UPLOAD_SUCCESS.value})
    except Exception as e:
        loger.error(f"File upload failed: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message":ResponseSignal.UPLOAD_FAILURE.value})