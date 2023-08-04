# _*_ coding: utf-8 _*_

"""
file api
"""

import time
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends, Form, Path, UploadFile
from fastapi import File as UploadFileClass  # rename File
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from core.settings import settings
from core.utils import get_id_string, iter_file
from data import get_session
from data.models import File, User
from data.schemas import FileSchema
from .utils import RespFile, check_file_permission
from ..utils import get_current_user

# define router
router = APIRouter()


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file object"),
            created_time: Optional[int] = Form(None, ge=946656000),
            updated_time: Optional[int] = Form(None, ge=946656000),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    upload file object and create file model, return file schema
    - **status_code=500**: file size too large
    """
    user_id = current_user.id
    file_kwargs = dict(created_time=created_time, updated_time=updated_time)

    # check file size or raise exception
    if file.size > settings.MAX_SIZE_FILE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large"
        )
    filename, filesize, filetype = file.filename, file.size, file.content_type
    file_kwargs.update(dict(filename=filename, filesize=filesize, filetype=filetype))

    # define fullname, location and save file
    fullname = f"{user_id}-{int(time.time())}-{filename}"
    location = f"{settings.FOLDER_FILE}/{fullname}"
    with open(location, "wb") as file_in:
        file_in.write(file.file.read())
    file_kwargs.update(dict(fullname=fullname, location=location))
    file_id = get_id_string(fullname)

    # create file model based on file_kwargs
    file_model = File(id=file_id, user_id=user_id, **file_kwargs)
    session.add(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.post("/upload-flow", response_model=RespFile)
def _upload_flow(file: UploadFile = UploadFileClass(..., description="part of file object"),
                 flow_chunk_number: int = Form(..., alias="flowChunkNumber"),
                 flow_chunk_total: int = Form(..., alias="flowChunkTotal"),
                 flow_total_size: int = Form(..., alias="flowTotalSize"),
                 flow_identifier: str = Form(..., alias="flowIdentifier"),
                 created_time: Optional[int] = Form(None, ge=946656000),
                 updated_time: Optional[int] = Form(None, ge=946656000),
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    """
    upload file object by flow.js, return file schema
    - **status_code=500**: file size too large
    """
    user_id = current_user.id
    file_kwargs = dict(created_time=created_time, updated_time=updated_time)

    # check file size or raise exception
    if flow_total_size > settings.MAX_SIZE_FILE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large",
        )
    filename_temp = file.filename

    # save flow_chunk_number part of file
    fullname_temp = f"{flow_identifier}-{filename_temp}"
    location_temp = f"{settings.FOLDER_FILE}/{fullname_temp}"
    file_mode = "ab" if flow_chunk_number > 1 else "wb"
    with open(location_temp, file_mode) as file_in:
        file_in.write(file.file.read())

    # check if all parts are uploaded
    if flow_chunk_number != flow_chunk_total:
        return RespFile(msg="uploading")
    filename, filesize, filetype = file.filename, file.size, file.content_type
    file_kwargs.update(dict(filename=filename, filesize=filesize, filetype=filetype))

    # define fullname, location and save file
    fullname = f"{user_id}-{int(time.time())}-{filename}"
    location = f"{settings.FOLDER_FILE}/{fullname}"
    with open(location, "wb") as file_in:
        with open(location_temp, "rb") as file_temp:
            file_in.write(file_temp.read())
    file_kwargs.update(dict(fullname=fullname, location=location))
    file_id = get_id_string(fullname)

    # create file model based on file_kwargs
    file_model = File(id=file_id, user_id=user_id, **file_kwargs)
    session.add(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.get("/download/{file_id}", response_class=FileResponse)
def _download(file_id: str = Path(..., description="id of file"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    download file object by file_id, return FileResponse
    - **status_code=403**: no permission to access file
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location

    # return file response
    return FileResponse(location, filename=filename)


@router.get("/download-stream/{file_id}", response_class=StreamingResponse)
def _download_stream(file_id: str = Path(..., description="id of file"),
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    download file object by file_id, return StreamingResponse
    - **status_code=403**: no permission to access file
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location

    # return streaming response
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}
    return StreamingResponse(iter_file(location), media_type="application/octet-stream", headers=headers)
