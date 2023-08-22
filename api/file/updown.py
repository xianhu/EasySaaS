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


@router.post("/upload", response_model=RespFile)
def _upload(file: UploadFile = UploadFileClass(..., description="file object"),
            filename: Optional[str] = Form(None, description="file name"),
            keywords: List[str] = Form([], description="keywords"),
            filetag_id_list: List[str] = Form([], description="filetag id list"),
            current_user: User = Depends(get_current_user),
            session: Session = Depends(get_session)):
    """
    upload file object and create file model, return file schema
    - **status=1**: file existed in database
    - **status=-1**: file count exceed limit
    - **status=-2**: filename invalid: xxx.xxx
    - **status=-3**: file type not supported
    - **status=-4**: file size exceed limit
    - **status_code=500**: create file or link to filetag error
    """
    user_id = current_user.id
    session_id = str(int(datetime.utcnow().timestamp() * 1000))

    # check if file model existed based on session_id
    file_id = get_id_string(f"{user_id}-{session_id}")
    file_model = session.query(File).get(file_id)
    if file_model and file_model.status == 1:
        file_schema = FileSchema(**file_model.dict())
        filetag_id_list = get_filetag_id_list(file_id, session)
        return RespFile(status=1, msg="file existed in database",
                        data_file=file_schema, data_filetag_id_list=filetag_id_list)

    # check if file count exceed limit
    filter0 = File.user_id == user_id
    if session.query(File).filter(filter0).count() >= FILE_LIMIT_COUNT:
        return RespFile(status=-1, msg="file count exceed limit")

    # check if filename valid
    filename = filename or file.filename
    if (not filename) or (filename.find(".") < 0):
        return RespFile(status=-2, msg="filename invalid: xxx.xxx")

    # check if file type not supported
    filetype = file.content_type
    if filetype not in ["audio/mpeg", "audio/wav", "audio/x-wav",
                        "audio/mp4", "audio/webm", "audio/x-m4a"]:
        return RespFile(status=-3, msg="file type (%s) not supported" % filetype)

    # check if file size exceed limit
    filesize = file.size
    if filesize > 1024 * 1024 * 25:
        return RespFile(status=-4, msg="file size (%s) exceed limit" % filesize)
    prefix = filename.split(".")[-1]

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


@router.get("/download/{file_id}", response_class=StreamingResponse)
def _download(file_id: str = Path(..., description="file id"),
              current_user: User = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    download file object by file_id, return StreamingResponse
    - **status_code=404**: file not found
    """
    # check file_id and get file model
    file_model = check_file(file_id, current_user.id, session)
    filename, location = file_model.filename, file_model.location
    filename_encoded = urllib_parse.quote(filename)

    # return streaming response with filename in headers
    headers = {"Content-Disposition": f"attachment; filename*=UTF-8''{filename_encoded}"}
    return StreamingResponse(iter_file(location), media_type="application/octet-stream", headers=headers)
