# _*_ coding: utf-8 _*_

"""
file api
"""

from .utils import *
from ..base import *
from ..filetag.utils import check_filetag
from ..utils import get_current_user

# define router
router = APIRouter()

# file settings
FILE_FOLDER = "/tmp"
FILE_LIMIT_COUNT = 10000


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file object"),
            filename: Optional[str] = Form(None, description="file name"),
            keywords: List[str] = Form([], description="keywords"),
            filetag_id_list: List[str] = Form([], description="filetag id list"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    upload file object and create file model, return file schema
    - **status_code=500**: file count exceed limit
    - **status_code=500**: file type not supported
    - **status_code=500**: file size too large
    - **status_code=500**: create file or link to filetag error
    """
    user_id = current_user.id
    filter0 = File.user_id == user_id

    # check if file count exceed limit
    if session.query(File).filter(filter0).count() >= FILE_LIMIT_COUNT:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file count exceed limit"
        )

    # check file type and size
    filetype, filesize = file.content_type, file.size
    check_file_type_size(filetype, filesize)

    # define default values
    filename = filename or file.filename or "noname.unknown"
    session_id = str(int(datetime.utcnow().timestamp() * 1000))
    prefix = filename.split(".")[-1] if "." in filename else filetype.split("/")[-1]

    # define fullname and location
    fullname = f"{user_id}-{session_id}.{prefix}"
    location = f"{FILE_FOLDER}/{fullname}"

    # save file to disk or cloud
    with open(location, "wb") as file_in:
        file_in.write(file.file.read())
    file_id = get_id_string(fullname)

    try:
        # create file model based on filename, keywords, ...
        file_schema = FileCreate(filename=filename, keywords=keywords)
        file_model = File(id=file_id, user_id=user_id, **file_schema.model_dump(exclude_unset=True),
                          filesize=filesize, filetype=filetype, fullname=fullname, location=location)
        session.add(file_model)

        # link to filetag based on filetags
        for filetag_id in filetag_id_list:
            check_filetag(filetag_id, user_id, session)

            # create filetagfile model by file_id and filetag_id
            filetagfile_model = FileTagFile(file_id=file_id, filetag_id=filetag_id)
            session.add(filetagfile_model)

        # commit session
        session.commit()
    except Exception as excep:
        session.rollback()
        logging.error("create file error: %s", excep)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="create file or link to filetag error",
        )

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = get_filetag_id_list(file_id, session)
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)


@router.get("/download/{file_id}", response_class=FileResponse)
def _download(file_id: str = Path(..., description="file id"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    download file object by file_id, return FileResponse
    - **status_code=404**: file not found
    """
    # check file_id and get file model
    file_model = check_file(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location

    # return file response with filename in headers
    return FileResponse(location, filename=filename, headers={"filename": filename})


@router.get("/download-stream/{file_id}", response_class=StreamingResponse)
def _download_stream(file_id: str = Path(..., description="file id"),
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    download file object by file_id, return StreamingResponse
    - **status_code=404**: file not found
    """
    # check file_id and get file model
    file_model = check_file(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location

    # return streaming response with filename in headers
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\"", "filename": filename}
    return StreamingResponse(iter_file(location), media_type="application/octet-stream", headers=headers)
