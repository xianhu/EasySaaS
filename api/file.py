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
from data.models import File, FileTagFile, User
from data.schemas import FileCreate, FileSchema, FileUpdate, Resp
from .filetag import check_filetag_permission
from .utils import get_current_user

# define router
router = APIRouter()


# response model
class RespFile(Resp):
    data_file: FileSchema = Field(None)
    data_filetag_id_list: List[str] = Field(None)


# response model
class RespFileList(Resp):
    data_file_list: List[FileSchema] = Field(None)
    data_filetag_id_list_list: List[List[str]] = Field(None)


def check_file_permission(file_id: str, user_id: str, session: Session) -> File:
    """
    check if file_id is valid and user_id has permission to access file
    """
    file_model = session.query(File).get(file_id)
    if (not file_model) or (file_model.user_id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no permission to access file",
        )
    return file_model


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file object"),
            file_schema: FileCreate = Body(..., description="create schema"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    upload file object based on create schema, return file schema
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

    # create file model based on create schema
    file_kwargs.update(file_schema.model_dump(exclude_unset=True))
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

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.get("/download/{file_id}", response_class=FileResponse)
def _download(file_id: str = Path(..., description="id of file"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    download file by file_id, return FileResponse
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
    download file by file_id, return StreamingResponse
    - **status_code=403**: no permission to access file
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
    - **status_code=403**: no permission to access file
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)

    # update file model based on update schema
    for field in file_schema.model_dump(exclude_unset=True):
        setattr(file_model, field, getattr(file_schema, field))
    session.merge(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.delete("/{file_id}", response_model=RespFile)
def _delete_file_model(file_id: str = Path(..., description="id of file"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    delete file by file_id, return file schema
    - **status_code=403**: no permission to access file
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)
    # delete file from disk and delete filetagfile model if necessary

    # delete file model
    session.delete(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(current_user: User = Depends(get_current_user)):
    """
    get file schema list and filetag_id list list of current_user
    """
    # file schema list and filetag_id list list
    file_schema_list, filetag_id_list_list = [], []
    for file_model in current_user.files:
        # define file schema and append to list
        file_schema = FileSchema(**file_model.dict())
        file_schema_list.append(file_schema)
        # define filetag_id list and append to list
        filetag_id_list = [ftfm.filetag_id for ftfm in file_model.filetagfiles]
        filetag_id_list_list.append(filetag_id_list)

    # return file schema list and filetag_id list list
    return RespFileList(data_file_list=file_schema_list, data_filetag_id_list_list=filetag_id_list_list)


@router.post("/link/", response_model=RespFile)
def _link_file_filetag(file_id: str = Body(..., description="id of file"),
                       filetag_id: str = Body(..., description="id of filetag"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    link file to a filetag, return file schema and filetag_id list
    - **status_code=403**: no permission to access file or filetag
    """
    # check file_id and get file model, filetag_id and get filetag model
    file_model = check_file_permission(file_id, current_user.id, session)
    filetag_model = check_filetag_permission(filetag_id, current_user.id, session)

    # check if filetagfile existed in database
    filetagfile_model = session.query(FileTagFile).filter(
        FileTagFile.file_id == file_id,
        FileTagFile.filetag_id == filetag_id,
    ).first()
    if not filetagfile_model:
        # create filetagfile model and save to database
        filetagfile_model = FileTagFile(file_id=file_id, filetag_id=filetag_id)
        session.add(filetagfile_model)
        session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = [ftfm.filetag_id for ftfm in file_model.filetagfiles]
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)


@router.post("/unlink/", response_model=RespFile)
def _unlink_file_filetag(file_id: str = Body(..., description="id of file"),
                         filetag_id: str = Body(..., description="id of filetag"),
                         current_user: User = Depends(get_current_user),
                         session: Session = Depends(get_session)):
    """
    unlink file from a filetag, return file schema and filetag_id list
    - **status_code=403**: no permission to access file or filetag
    """
    # check file_id and get file model, filetag_id and get filetag model
    file_model = check_file_permission(file_id, current_user.id, session)
    filetag_model = check_filetag_permission(filetag_id, current_user.id, session)

    # delete filetagfile model
    session.query(FileTagFile).filter(
        FileTagFile.file_id == file_id,
        FileTagFile.filetag_id == filetag_id,
    ).delete()
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = [ftfm.filetag_id for ftfm in file_model.filetagfiles]
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)
