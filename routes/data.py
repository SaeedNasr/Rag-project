from fastapi import Depends, FastAPI, APIRouter ,UploadFile,status , Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings,Settings
from controllers import DataController ,ProjectController ,ProcessController
import aiofiles
from models import ResponseSignal
import logging 
from .schemes.data import ProcessRequst
loger = logging.getLogger("uvicorn.error")
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk
data_router = APIRouter(prefix="/api/v1/data",
                         tags=["api_v1",["data"]])

@data_router.post("/upload/{project_id}")

async def upload_data(request:Request,project_id:str,file:UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_create_project(project_id=project_id)

    datacontroller = DataController()
    projectcontroller = ProjectController()
    is_valid ,result_signal= datacontroller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message":result_signal.value})
    
    project_dir_path = projectcontroller.get_project_path(project_id=project_id)
    file_path ,file_id= datacontroller.generate_unique_file_path(original_filename=file.filename,
                                                  project_id=project_id)
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content= {"Signal" : ResponseSignal.UPLOAD_SUCCESS.value,
                                  "file_id":file_id})
    except Exception as e:
        loger.error(f"File upload failed: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"message":ResponseSignal.UPLOAD_FAILURE.value})

    
@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,process_request:ProcessRequst):
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_or_create_project(project_id=project_id)
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    
    processcontroller = ProcessController(project_id=project_id)
    file_content = processcontroller.get_file_content(file_id=file_id)
    file_chunks = processcontroller.process_file(file_id=file_id,
                                                 file_content=file_content,chunk_Size=chunk_size,
                                                 overlap_size=overlap_size)
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message":ResponseSignal.FILE_PROCESSING_FAILURE.value})
    
    file_chunks_records = [DataChunk(
    chunk_text= chunk.page_content,
    chunk_metadata = chunk.metadata,
    chunk_order = i+1,
    chunk_project_id=project.id) 
    for i,chunk in enumerate(file_chunks)]
    chunk_model = ChunkModel(db_client=request.app.db_client)

    if do_reset:
        deleted_count = await chunk_model.delete_chunks_by_project(project_id=project.id)
        loger.info(f"Deleted {deleted_count} chunks for project {project_id} during reset.")
        
    record_count = await chunk_model.insert_many_chunks(chunks=file_chunks_records, batch_size=100)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message":ResponseSignal.FILE_PROCESSING_SUCCESS.value,
                                 "total_chunks_created":record_count})