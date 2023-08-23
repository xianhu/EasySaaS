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


@router.get("/", response_model=RespFileList)
def _get_file_schema_list(skip: int = Query(0, description="skip count"),
                          limit: int = Query(100, description="limit count"),
                          is_trash: bool = Query(False, description="is trash"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    get file schema list, support pagination
    - **status_code=500**: delete file filetagfile error
    """
    user_id = current_user.id
    filter0 = sqlalchemy.and_(File.user_id == user_id, File.is_trash == is_trash)

    # delete file model if is_trash is True
    if is_trash:
        # delete file model if (now - trash_time) > 30 days
        filter1 = File.trash_time < datetime.utcnow() - timedelta(days=30)
        file_model_list = session.query(File).filter(filter0, filter1).all()
        delete_file_filetagfile([file_model.id for file_model in file_model_list], session)

    # get file schema list
    file_schema_list = []
    for file_model in (session.query(File).filter(filter0)
            .order_by(File.created_at.desc())
            .offset(skip).limit(limit).all()):
        file_schema = FileSchema(**file_model.dict())
        file_schema.filetag_id_list = get_filetag_id_list(file_model.id, session)
        file_schema_list.append(file_schema)

    # return total count and file schema list
    file_total = session.query(File).filter(filter0).count()
    return RespFileList(data_file_total=file_total, data_file_list=file_schema_list)


@router.get("/{file_id}", response_model=RespFile)
def _get_file_schema(file_id: str = Path(..., description="file id"),
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    get file schema by file_id
    - **status_code=404**: file not found
    """
    user_id = current_user.id

    # check file_id and get file model
    file_model = check_file(file_id, user_id, session)

    # create file schema
    file_schema = FileSchema(**file_model.dict())
    file_schema.filetag_id_list = get_filetag_id_list(file_id, session)

    # return file schema
    return RespFile(data_file=file_schema)


@router.patch("/{file_id}", response_model=RespFile)
def _update_file_model(file_id: str = Path(..., description="file id"),
                       file_schema: FileUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    update file model based on update schema, return file schema
    - **status_code=404**: file not found or filetag not found
    - **status_code=500**: update file or link to filetag error
    """
    user_id = current_user.id
    filetag_id_list = file_schema.filetag_id_list

    # check file_id and get file model
    file_model = check_file(file_id, user_id, session)

    # check filetag_id_list
    for filetag_id in filetag_id_list:
        check_filetag(filetag_id, user_id, session)

    try:
        # unlink based on filetag_id_list
        filter1 = FileTagFile.file_id == file_id
        filter2 = FileTagFile.filetag_id.notin_(filetag_id_list)
        session.query(FileTagFile).filter(filter1, filter2).delete()

        # link to filetag based on filetags
        for filetag_id in file_schema.filetag_id_list:
            filter1 = FileTagFile.file_id == file_id
            filter2 = FileTagFile.filetag_id == filetag_id
            if session.query(FileTagFile).filter(filter1, filter2).first():
                continue

            # create filetagfile model by file_id and filetag_id
            filetagfile_model = FileTagFile(file_id=file_id, filetag_id=filetag_id)
            session.add(filetagfile_model)

        # update file model based on update schema
        for field in file_schema.model_dump(exclude_unset=True):
            if field == "filetag_id_list":
                continue
            setattr(file_model, field, getattr(file_schema, field))

        # update edit_time based on utcnow
        file_model.edit_time = datetime.utcnow()
        session.merge(file_model)

        # commit session
        session.commit()
    except Exception as excep:
        session.rollback()
        logging.error("update file error: %s", excep)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="update file or link to filetag error",
        )

    # create file schema
    file_schema = FileSchema(**file_model.dict())
    file_schema.filetag_id_list = get_filetag_id_list(file_id, session)

    # return file schema
    return RespFile(data_file=file_schema)


@router.post("/trash/", response_model=Resp)
def _trash_file_model_list(file_id_list: List[str] = Body(..., description="list of file id"),
                           current_user: User = Depends(get_current_user),
                           session: Session = Depends(get_session)):
    """
    trash file model list by file_id list
    """
    user_id = current_user.id
    filter0 = sqlalchemy.and_(File.user_id == user_id, File.is_trash == False)

    # trash file model list by file_id list
    filter1 = File.id.in_(file_id_list)
    update_dict = {File.is_trash: True, File.trash_time: datetime.utcnow()}
    session.query(File).filter(filter0, filter1).update(update_dict)
    session.commit()

    # return result
    return Resp(msg="trash success")


@router.post("/untrash/", response_model=Resp)
def _untrash_file_model_list(file_id_list: List[str] = Body(..., description="list of file id"),
                             current_user: User = Depends(get_current_user),
                             session: Session = Depends(get_session)):
    """
    untrash file model list by file_id list
    """
    user_id = current_user.id
    filter0 = sqlalchemy.and_(File.user_id == user_id, File.is_trash == True)

    # untrash file model list by file_id list
    filter1 = File.id.in_(file_id_list)
    update_dict = {File.is_trash: False, File.trash_time: None}
    session.query(File).filter(filter0, filter1).update(update_dict)
    session.commit()

    # return result
    return Resp(msg="untrash success")


@router.delete("/", response_model=Resp)
def _delete_file_model_list(file_id_list: List[str] = Body(..., description="list of file id"),
                            current_user: User = Depends(get_current_user),
                            session: Session = Depends(get_session)):
    """
    delete file model list by file_id list
    - **status_code=500**: delete file filetagfile error
    """
    user_id = current_user.id
    filter0 = sqlalchemy.and_(File.user_id == user_id, File.is_trash == True)

    # delete file model list by file_id list
    filter1 = File.id.in_(file_id_list)
    file_model_list = session.query(File).filter(filter0, filter1).all()
    delete_file_filetagfile([file_model.id for file_model in file_model_list], session)

    # return result
    return Resp(msg="delete success")
