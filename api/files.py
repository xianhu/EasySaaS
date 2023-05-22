# _*_ coding: utf-8 _*_

"""
files api
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from core.settings import settings
from data.models import User
from data.schemas import Resp
from .utils import get_current_user

# define router
router = APIRouter()


@router.post("/upload", response_model=Resp)
def _upload(file: UploadFile = File(...),
            current_user: User = Depends(get_current_user)):
    """
    upload file
    """
    # check file size
    if file.size > settings.MAX_FILE_SIZE:
        return Resp(status=-1, msg="file size too large")

    # define file path and save file
    file_name = f"{current_user.id}_{file.filename}"
    file_path = f"{settings.FOLDER_UPLOAD}/{file_name}"
    with open(file_path, "wb") as file_in:
        file_in.write(file.file.read())

    # return result
    return Resp(msg="upload success")


@router.post("/upload-multi", response_model=Resp)
def _upload_multi(files: list[UploadFile] = File(...),
                  current_user: User = Depends(get_current_user)):
    """
    upload multi files
    """
    for file in files:
        # check file size
        if file.size > settings.MAX_FILE_SIZE:
            return Resp(status=-1, msg="file size too large")

        # define file path and save file
        file_name = f"{current_user.id}_{file.filename}"
        file_path = f"{settings.FOLDER_UPLOAD}/{file_name}"
        with open(file_path, "wb") as file_in:
            file_in.write(file.file.read())

    # return result
    return Resp(msg="upload success")


@router.post("/upload-flow", response_model=Resp)
def _upload_flow(file: UploadFile = File(...),
                 flow_chunk_number: int = Form(..., alias="flowChunkNumber"),
                 flow_chunk_total: int = Form(..., alias="flowChunkTotal"),
                 flow_total_size: int = Form(..., alias="flowTotalSize"),
                 current_user: User = Depends(get_current_user)):
    """
    upload file by flow.js
    """
    # check file size: raise exception
    if flow_total_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file size too large",
        )

    # define file path and save file
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
