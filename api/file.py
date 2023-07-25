# _*_ coding: utf-8 _*_

"""
file api
"""

import os
import time

from fastapi import APIRouter, HTTPException, status
from fastapi import Body, Depends, Form, Path, UploadFile
from fastapi import File as UploadFileClass  # rename File
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import Field
from sqlalchemy.orm import Session

from core.settings import settings
from core.utils import get_id_string, iter_file
from data import get_session
from data.models import File, FileTagFile, User
from data.schemas import FileSchema, FileUpdate, Resp
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFile(Resp):
    data: FileSchema = Field(None)


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file object"),
            filetag_id: str = Body(..., embed=True, description="id of filetag"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    upload file object, return file schema
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
    filesize = file.size
    file_id = get_id_string(fullname)
    filetagfile_id = get_id_string(f"{filetag_id}-{file_id}")

    # create file model and save to database
    file_model = File(id=file_id,
                      filename=filename, filesize=filesize,
                      fullname=fullname, location=location)
    filetagfile_model = FileTagFile(id=filetagfile_id, filetag_id=filetag_id, file_id=file_id)
    session.add_all([file_model, filetagfile_model])
    session.commit()

    # return file schema with permission
    return RespFile(data=FileSchema(**file_model.dict()))


@router.post("/upload-flow", response_model=RespFile)
def _upload_flow(file: UploadFile = UploadFileClass(..., description="part of file object"),
                 flow_chunk_number: int = Form(..., alias="flowChunkNumber"),
                 flow_chunk_total: int = Form(..., alias="flowChunkTotal"),
                 flow_total_size: int = Form(..., alias="flowTotalSize"),
                 flow_identifier: str = Form(..., alias="flowIdentifier"),
                 filetag_id: str = Form(..., description="id of filetag"),
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    """
    upload file object by flow.js, return file schema
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
    filesize = flow_total_size
    file_id = get_id_string(fullname)
    filetagfile_id = get_id_string(f"{filetag_id}-{file_id}")

    # create file model and save to database
    file_model = File(id=file_id,
                      filename=filename, filesize=filesize,
                      fullname=fullname, location=location)
    filetagfile_model = FileTagFile(id=filetagfile_id, filetag_id=filetag_id, file_id=file_id)
    session.add_all([file_model, filetagfile_model])
    session.commit()

    # return file schema with permission
    return RespFile(data=FileSchema(**file_model.dict()))


@router.patch("/{file_id}", response_model=RespFile)
def _patch(file_id: str = Path(..., description="id of file"),
           file_schema: FileUpdate = Body(..., description="update schema"),
           current_user: User = Depends(get_current_user),
           session: Session = Depends(get_session)):
    """
    update file model based on update schema, return file schema
    - **status=-1**: file not existed
    """
    # check if file existed
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != current_user.id):
        return Resp(status=-1, msg="file not existed")

    # update file model
    for field in file_schema.model_dump(exclude_unset=True):
        setattr(file_model, field, getattr(file_schema, field))
    session.merge(file_model)
    session.commit()

    # return file schema with permission
    return RespFile(data=FileSchema(**file_model.dict()))


@router.get("/{file_id}", response_class=FileResponse)
def _download(file_id: str = Path(..., description="id of file"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    download file by file_id, return FileResponse
    - **status_code=500**: file not existed
    """
    # check if file existed
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != current_user.id):
        return Resp(status=-1, msg="file not existed")
    location = file_model.location

    # check if file existed
    if not os.path.exists(location):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file not existed",
        )
    filename = "-".join(file_id.split("-")[2:])

    # return file response
    return FileResponse(location, filename=filename)


@router.get("/stream/{file_id}", response_class=StreamingResponse)
def _download_stream(file_id: str = Path(..., description="id of file"),
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    download file by file_id, return StreamingResponse
    - **status_code=500**: file not existed
    """
    # check if file existed
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != current_user.id):
        return Resp(status=-1, msg="file not existed")
    location = file_model.location

    # check if file existed
    if not os.path.exists(location):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file not existed",
        )
    filename = "-".join(file_id.split("-")[2:])

    # return streaming response
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}
    return StreamingResponse(iter_file(location), media_type="application/octet-stream", headers=headers)
