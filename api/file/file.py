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
    get file schema list and filetag_id list list, support pagination
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

    # get file model list and schema list
    file_model_list = (session.query(File).filter(filter0)
                       .order_by(File.created_at.desc())
                       .offset(skip).limit(limit).all())
    file_schema_list = [FileSchema(**fm.dict()) for fm in file_model_list]

    # return total count, file schema list and filetag_id list list
    file_total = session.query(File).filter(filter0).count()
    filetag_id_list_list = [get_filetag_id_list(fm.id, session) for fm in file_model_list]
    return RespFileList(data_file_total=file_total, data_file_list=file_schema_list, data_filetag_id_list_list=filetag_id_list_list)


@router.get("/{file_id}", response_model=RespFile)
def _get_file_schema(file_id: str = Path(..., description="file id"),
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    get file schema and filetag_id list by file_id
    - **status_code=404**: file not found
    """
    user_id = current_user.id

    # check file_id and get file model
    file_model = check_file(file_id, user_id, session)

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = get_filetag_id_list(file_id, session)
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)


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

    # check file_id and get file model
    file_model = check_file(file_id, user_id, session)

    # check filetag_id_list
    for filetag_id in file_schema.filetag_id_list:
        check_filetag(filetag_id, user_id, session)

    try:
        # link to filetag based on filetags
        for filetag_id in file_schema.filetag_id_list:
            # create filetagfile model by file_id and filetag_id
            filetagfile_model = FileTagFile(file_id=file_id, filetag_id=filetag_id)
            session.add(filetagfile_model)

        # update file model based on update schema
        for field in file_schema.model_dump(exclude_unset=True):
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

    # return file schema and filetag_id list
    file_schema = FileSchema(**file_model.dict())
    filetag_id_list = get_filetag_id_list(file_id, session)
    return RespFile(data_file=file_schema, data_filetag_id_list=filetag_id_list)


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
