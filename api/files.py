# _*_ coding: utf-8 _*_

"""
files api
"""

from fastapi import APIRouter, Depends, UploadFile

from core.settings import settings
from data.models import User
from data.schemas import Result
from .utils import get_current_user

# define router
router = APIRouter()


@router.post("/upload", response_model=Result)
def _upload(file: UploadFile, current_user: User = Depends(get_current_user)):
    """
    upload file: flowChunkNumber/flowTotalChunks/...for flow.js
    """
    file_name = f"{current_user.id}_{file.filename}"
    with open(f"{settings.FOLDER_UPLOAD}/{file_name}", "wb") as file_in:
        file_in.write(file.file.read())
    return Result(msg="upload success")
