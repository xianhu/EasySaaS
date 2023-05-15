# _*_ coding: utf-8 _*_

"""
files api
"""

from fastapi import APIRouter, Request, UploadFile

from core.settings import settings
from data.schemas import Result

# define router
router = APIRouter()


@router.post("/upload", response_model=Result)
def _upload(file: UploadFile, request: Request):
    """
    upload file
    """
    file_path = f"{settings.FOLDER_UPLOAD}/{file.filename}"
    with open(file_path, "wb") as file_in:
        file_in.write(file.file.read())
    return Result(msg="upload success")
