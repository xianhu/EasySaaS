# _*_ coding: utf-8 _*_

"""
file api
"""

import os
import time

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends, Form, Path, UploadFile
from fastapi import File as UploadFileClass  # rename File
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import Field

from core.settings import settings
from core.utility import iter_file
from data.models import User
from data.schemas import FileSchema, Resp
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFile(Resp):
    data: FileSchema = Field(None)


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file"),
            current_user: User = Depends(get_current_user)):
    """
    upload file, return file schema
    - **status=0**: upload success
    - **status=-1**: upload failed
    - **status_code=500**: file size too large
    """
    # check file size or raise exception
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large"
        )
    filename = file.filename

    # define fullname, location and save file
    fullname = f"{current_user.id}-{int(time.time())}-{filename}"
    location = f"{settings.FOLDER_UPLOAD}/{fullname}"
    with open(location, "wb") as file_in:
        file_in.write(file.file.read())
    # save file model (filename, fullname, location) to database

    # return FileSchema with permission
    return RespFile(data=FileSchema(filename=filename))


@router.post("/upload-flow", response_model=RespFile)
def _upload_flow(file: UploadFile = UploadFileClass(..., description="part of file"),
                 flow_chunk_number: int = Form(..., alias="flowChunkNumber"),
                 flow_chunk_total: int = Form(..., alias="flowChunkTotal"),
                 flow_total_size: int = Form(..., alias="flowTotalSize"),
                 flow_identifier: str = Form(..., alias="flowIdentifier"),
                 current_user: User = Depends(get_current_user)):
    """
    upload file by flow.js, return file schema
    - **status=0**: upload success
    - **status=-1**: upload failed
    - **status_code=500**: file size too large
    """
    # check file size or raise exception
    if flow_total_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large",
        )
    filename_temp = file.filename

    # save flow_chunk_number part of file
    fullname_temp = f"{flow_identifier}-{filename_temp}"
    location_temp = f"{settings.FOLDER_UPLOAD}/{fullname_temp}"
    file_mode = "ab" if flow_chunk_number > 1 else "wb"
    with open(location_temp, file_mode) as file_in:
        file_in.write(file.file.read())

    # check if all parts are uploaded
    if flow_chunk_number != flow_chunk_total:
        return RespFile(msg="uploading")
    filename = file.filename

    # define fullname, location and save file
    fullname = f"{current_user.id}-{int(time.time())}-{filename}"
    location = f"{settings.FOLDER_UPLOAD}/{fullname}"
    with open(location, "wb") as file_in:
        with open(location_temp, "rb") as file_temp:
            file_in.write(file_temp.read())
    # save file model (filename, fullname, location) to database

    # return FileSchema with permission
    return RespFile(data=FileSchema(filename=filename))


@router.get("/download/{file_id}", response_class=FileResponse)
def _download(file_id: str = Path(..., description="file id")):
    """
    download file by file_id, return FileResponse
    - **status_code=500**: file not existed
    """
    # define location and check if file existed
    location = f"{settings.FOLDER_UPLOAD}/{file_id}"
    if not os.path.exists(location):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file not existed",
        )
    filename = "-".join(file_id.split("-")[2:])

    # return file response
    return FileResponse(location, filename=filename)


@router.get("/download-stream/{file_id}", response_class=StreamingResponse)
def _download_stream(file_id: str = Path(..., description="file id")):
    """
    download file by file_id, return StreamingResponse
    - **status_code=500**: file not existed
    """
    # define location and check if file existed
    location = f"{settings.FOLDER_UPLOAD}/{file_id}"
    if not os.path.exists(location):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file not existed",
        )
    filename = "-".join(file_id.split("-")[2:])

    # return streaming response
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}
    return StreamingResponse(iter_file(location), media_type="application/octet-stream", headers=headers)
