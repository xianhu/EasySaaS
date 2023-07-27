# _*_ coding: utf-8 _*_

"""
file api
"""

import time
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi import Body, Depends, Form, Path, UploadFile
from fastapi import File as UploadFileClass  # rename File
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import Field
from sqlalchemy.orm import Session

from core.settings import settings
from core.utils import get_id_string, iter_file
from data import get_session
from data.models import File, User
from data.schemas import FileSchema, FileUpdate, Resp
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFile(Resp):
    data_file: FileSchema = Field(None)


# response model
class RespFileList(Resp):
    data_file_list: List[FileSchema] = Field(None)


def check_file_permission(file_id: str, user_id: str, session: Session) -> File:
    """
    check if file_id is valid and user_id has permission to access file
    """
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file not existed",
        )
    return file_model


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file object"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    upload file object, return file schema
    - **status_code=500**: file size too large
    """
    user_id = current_user.id

    # check file size or raise exception
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large"
        )
    filename, filesize = file.filename, file.size
    file_kwargs = dict(filename=filename, filesize=filesize)

    # define fullname, location and save file
    fullname = f"{user_id}-{int(time.time())}-{filename}"
    location = f"{settings.FOLDER_UPLOAD}/{fullname}"
    with open(location, "wb") as file_in:
        file_in.write(file.file.read())
    file_kwargs.update(dict(fullname=fullname, location=location))
    file_id = get_id_string(fullname)

    # create file model and save to database
    file_model = File(id=file_id, user_id=user_id, **file_kwargs)
    session.add(file_model)
    session.commit()

    # return file schema
    return RespFile(data_file=FileSchema(**file_model.dict()))


@router.post("/upload-flow", response_model=RespFile)
def _upload_flow(file: UploadFile = UploadFileClass(..., description="part of file object"),
                 flow_chunk_number: int = Form(..., alias="flowChunkNumber"),
                 flow_chunk_total: int = Form(..., alias="flowChunkTotal"),
                 flow_total_size: int = Form(..., alias="flowTotalSize"),
                 flow_identifier: str = Form(..., alias="flowIdentifier"),
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    """
    upload file object by flow.js, return file schema
    - **status_code=500**: file size too large
    """
    user_id = current_user.id

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
    filename, filesize = file.filename, file.size
    file_kwargs = dict(filename=filename, filesize=filesize)

    # define fullname, location and save file
    fullname = f"{user_id}-{int(time.time())}-{filename}"
    location = f"{settings.FOLDER_UPLOAD}/{fullname}"
    with open(location, "wb") as file_in:
        with open(location_temp, "rb") as file_temp:
            file_in.write(file_temp.read())
    file_kwargs.update(dict(fullname=fullname, location=location))
    file_id = get_id_string(fullname)

    # create file model and save to database
    file_model = File(id=file_id, user_id=user_id, **file_kwargs)
    session.add(file_model)
    session.commit()

    # return file schema
    return RespFile(data_file=FileSchema(**file_model.dict()))


@router.get("/download/{file_id}", response_class=FileResponse)
def _download(file_id: str = Path(..., description="id of file"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    download file by file_id, return FileResponse
    - **status_code=500**: file not existed
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
    download file by file_id, return StreamingResponse
    - **status_code=500**: file not existed
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location

    # return streaming response
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}
    return StreamingResponse(iter_file(location), media_type="application/octet-stream", headers=headers)


@router.patch("/{file_id}", response_model=RespFile)
def _update_file_model(file_id: str = Path(..., description="id of file"),
                       file_schema: FileUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    update file model based on update schema, return file schema
    - **status_code=500**: file not existed
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)

    # update file model
    for field in file_schema.model_dump(exclude_unset=True):
        setattr(file_model, field, getattr(file_schema, field))
    session.merge(file_model)
    session.commit()

    # return file schema
    return RespFile(data_file=FileSchema(**file_model.dict()))


@router.delete("/{file_id}", response_model=RespFile)
def _delete_file_model(file_id: str = Path(..., description="id of file"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    delete file by file_id, return file schema
    - **status_code=500**: file not existed
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)

    # delete file model
    session.delete(file_model)
    session.commit()

    # return file schema
    return RespFile(data_file=FileSchema(**file_model.dict()))


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    get file schema list of current_user, return file schema list
    """
    # file schema list
    file_schema_list = []
    for file_model in current_user.files:
        file_schema = FileSchema(**file_model.dict())
        file_schema_list.append(file_schema)

    # return file schema list
    return RespFileList(data_file_list=file_schema_list)


@router.post("/link/{file_id}", response_model=RespFile)
def _link_file_filetag_list(file_id: str = Path(..., description="id of file"),
                            filetag_id_list: str = Body(..., description="list of filetag_id"),
                            current_user: User = Depends(get_current_user),
                            session: Session = Depends(get_session)):
    """
    link file to filetag list, return file schema
    """
    raise NotImplementedError


@router.post("/unlink/{file_id}", response_model=RespFile)
def _unlink_file_filetag_list(file_id: str = Path(..., description="id of file"),
                              filetag_id_list: str = Body(..., description="list of filetag_id"),
                              current_user: User = Depends(get_current_user),
                              session: Session = Depends(get_session)):
    """
    unlink file from filetag list, return file schema
    """
    raise NotImplementedError
