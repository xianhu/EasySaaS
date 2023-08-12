# _*_ coding: utf-8 _*_

"""
file api
"""

from .utils import *
from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()

# file settings
FILE_FOLDER = "/tmp"
FILE_MAX_SIZE = 1024 * 1024 * 25
FILE_TYPE_LIST = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/x-m4a"]


def check_file_type_size(filetype: str, filesize: int) -> None:
    """
    check file type and size, raise exception or return None
    """
    if filetype not in FILE_TYPE_LIST:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file type not supported"
        )
    if filesize > FILE_MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large"
        )
    return None


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file object"),
            filename: Optional[str] = Form(None, description="file name"),
            keywords: Optional[str] = Form(None, description="keywords"),
            duration: Optional[int] = Form(None, description="duration of file"),
            start_time: Optional[datetime] = Form(None, description="2020-01-01T00:00:00"),
            end_time: Optional[datetime] = Form(None, description="2020-01-01T00:00:00"),
            timezone: Optional[int] = Form(None, description="-2, -1, 0, 1, 2"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    upload file object and create file model, return file schema
    - **status_code=500**: file type not supported, file size too large
    """
    user_id = current_user.id

    # check file type and size
    filesize, filetype = file.size, file.content_type
    check_file_type_size(filetype, filesize)

    # define filename, fullname, location
    filename = filename or file.filename
    fullname = f"{user_id}-{int(time.time())}-{filename}"
    location = f"{FILE_FOLDER}/{fullname}"
    with open(location, "wb") as file_in:
        file_in.write(file.file.read())
    file_id = get_id_string(fullname)

    # create file schema based on filename, keywords, duration, ...
    keywords = [i.strip() for i in (keywords.split(",") if keywords else [])]
    file_schema = FileCreate(filename=filename, keywords=keywords, duration=duration,
                             start_time=start_time, end_time=end_time, timezone=timezone)

    # create file model based on file_kwargs
    file_model = File(id=file_id, user_id=user_id, **file_schema.model_dump(exclude_unset=True),
                      filesize=filesize, filetype=filetype, fullname=fullname, location=location)
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
                 filename: Optional[str] = Form(None, description="file name"),
                 keywords: Optional[str] = Form(None, description="keywords"),
                 duration: Optional[int] = Form(None, description="duration of file"),
                 start_time: Optional[datetime] = Form(None, description="2020-01-01T00:00:00"),
                 end_time: Optional[datetime] = Form(None, description="2020-01-01T00:00:00"),
                 timezone: Optional[int] = Form(None, description="-2, -1, 0, 1, 2"),
                 current_user: User = Depends(get_current_user),
                 session: Session = Depends(get_session)):
    """
    upload file object by flow.js, return file schema
    - **status_code=500**: file type not supported, file size too large
    """
    user_id = current_user.id

    # check file type and size
    filesize, filetype = flow_total_size, file.content_type
    check_file_type_size(filetype, filesize)

    # define filename, fullname, location
    filename = filename or file.filename
    fullname = f"{user_id}-{flow_identifier}-{filename}"
    location = f"{FILE_FOLDER}/{fullname}"
    file_mode = "ab" if flow_chunk_number > 1 else "wb"
    with open(location, file_mode) as file_in:
        file_in.write(file.file.read())
    file_id = get_id_string(fullname)

    # check if all parts are uploaded
    if flow_chunk_number != flow_chunk_total:
        return RespFile(msg="uploading")

    # create file schema based on filename, keywords, duration, ...
    keywords = [i.strip() for i in (keywords.split(",") if keywords else [])]
    file_schema = FileCreate(filename=filename, keywords=keywords, duration=duration,
                             start_time=start_time, end_time=end_time, timezone=timezone)

    # create file model based on file_kwargs
    file_model = File(id=file_id, user_id=user_id, **file_schema.model_dump(exclude_unset=True),
                      filesize=filesize, filetype=filetype, fullname=fullname, location=location)
    session.add(file_model)
    session.commit()

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    return RespFile(data_file=file_schema, data_filetag_id_list=[])


@router.get("/download/{file_id}", response_class=FileResponse)
def _download(file_id: str = Path(..., description="file id"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    download file object by file_id, return FileResponse
    - **status_code=404**: file not found
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location

    # return file response
    return FileResponse(location, filename=filename)


@router.get("/download-stream/{file_id}", response_class=StreamingResponse)
def _download_stream(file_id: str = Path(..., description="file id"),
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    download file object by file_id, return StreamingResponse
    - **status_code=404**: file not found
    """
    # check file_id and get file model
    file_model = check_file_permission(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location

    # return streaming response
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}
    return StreamingResponse(iter_file(location), media_type="application/octet-stream", headers=headers)
