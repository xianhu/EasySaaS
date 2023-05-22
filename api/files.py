# _*_ coding: utf-8 _*_

"""
files api
"""

from fastapi import APIRouter, Depends, File, Form, UploadFile

from core.settings import settings
from data.models import User
from data.schemas import Resp
from .utils import get_current_user

# define router
router = APIRouter()


@router.post("/upload", response_model=Resp)
def _upload(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    upload file
    """
    file_name = f"{current_user.id}_{file.filename}"
    file_path = f"{settings.FOLDER_UPLOAD}/{file_name}"
    with open(file_path, "wb") as file_in:
        file_in.write(file.file.read())
    return Result(msg="upload success")


@router.post("/upload-multi", response_model=Resp)
def _upload_multi(files: list[UploadFile] = File(...), current_user: User = Depends(get_current_user)):
    """
    upload multi files
    """
    for file in files:
        file_name = f"{current_user.id}_{file.filename}"
        file_path = f"{settings.FOLDER_UPLOAD}/{file_name}"
        with open(file_path, "wb") as file_in:
            file_in.write(file.file.read())
    return Result(msg="upload success")


@router.post("/upload-flow", response_model=Resp)
def _upload_flow(file: UploadFile = File(...),
                 flow_chunk_number: int = Form(...),
                 flow_chunk_total: int = Form(...),
                 current_user: User = Depends(get_current_user)):
    """
    upload file by flow.js
    """
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
