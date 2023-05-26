# _*_ coding: utf-8 _*_

"""
files api
"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Security, status
from fastapi import File, Form, Path, UploadFile
from fastapi.responses import FileResponse

from core.settings import settings
from data.models import User
from data.schemas import Resp
from .utils import get_current_user

# define router
router = APIRouter()


@router.post("/upload", response_model=Resp)
def _upload(current_user: Annotated[User, Security(get_current_user, scopes=["files"])],
            file: UploadFile = File(...)):
    """
    upload file
    - **status=0**: upload success
    - **status=-1**: file size too large
    """
    # check file size
    if file.size > settings.MAX_FILE_SIZE:
        return Resp(status=-1, msg="file size too large")

    # define file path
    file_name = f"{current_user.id}_{file.filename}"
    file_path = f"{settings.FOLDER_UPLOAD}/{file_name}"

    # save file and return result
    with open(file_path, "wb") as file_in:
        file_in.write(file.file.read())
    return Resp(msg="upload success")


@router.post("/upload-flow", response_model=Resp)
def _upload_flow(current_user: Annotated[User, Security(get_current_user, scopes=["files"])],
                 file: UploadFile = File(...),
                 flow_chunk_number: int = Form(..., alias="flowChunkNumber"),
                 flow_chunk_total: int = Form(..., alias="flowChunkTotal"),
                 flow_total_size: int = Form(..., alias="flowTotalSize")):
    """
    upload file by flow.js
    - **status=0**: upload success
    - **status_code=400**: file size too large
    """
    # check file size: raise exception
    if flow_total_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file size too large",
        )

    # define file path
    file_name = f"{current_user.id}_{file.filename}"
    file_path = f"{settings.FOLDER_UPLOAD}/{file_name}"

    # save flow_chunk_number part
    file_mode = "ab" if flow_chunk_number > 1 else "wb"
    with open(file_path, file_mode) as file_in:
        file_in.write(file.file.read())

    # check if all parts are uploaded
    if flow_chunk_number != flow_chunk_total:
        return Resp(msg="uploading")
    return Resp(msg="upload success")


@router.get("/download/{file_name}", response_class=FileResponse)
def _download(current_user: Annotated[User, Security(get_current_user, scopes=["files"])],
              file_name: str = Path(...)):
    """
    download file
    """
    # define file path
    file_name = f"{current_user.id}_{file_name}"
    file_path = f"{settings.FOLDER_UPLOAD}/{file_name}"

    # return file response
    return FileResponse(file_path, filename=file_name)
