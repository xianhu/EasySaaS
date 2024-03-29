# _*_ coding: utf-8 _*_

"""
filetag api
"""

from .utils import *
from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()


@router.get("/", response_model=RespFileTagList)
def _get_filetag_schema_list(skip: int = Query(0, description="skip count"),
                             limit: int = Query(100, description="limit count"),
                             current_user: User = Depends(get_current_user),
                             session: Session = Depends(get_session)):
    """
    get filetag schema list, support pagination
    """
    user_id = current_user.id
    filter0 = FileTag.user_id == user_id

    # get filetag schema list
    filetag_schema_list = []
    for file_model in (session.query(FileTag).filter(filter0)
            .order_by(FileTag.created_at.desc())
            .offset(skip).limit(limit).all()):
        filetag_schema = FileTagSchema(**file_model.dict())
        filetag_schema_list.append(filetag_schema)

    # return total count and filetag schema list
    filetag_total = session.query(FileTag).filter(filter0).count()
    return RespFileTagList(data_filetag_total=filetag_total, data_filetag_list=filetag_schema_list)


@router.get("/{filetag_id}", response_model=RespFileTag)
def _get_filetag_schema(filetag_id: str = Path(..., description="filetag id"),
                        current_user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    """
    get filetag schema by filetag_id
    - **status_code=404**: filetag not found
    """
    user_id = current_user.id

    # check filetag_id and get filetag model
    filetag_model = check_filetag(filetag_id, user_id, session)

    # return filetag schema
    return RespFileTag(data_filetag=FileTagSchema(**filetag_model.dict()))


@router.post("/", response_model=RespFileTag)
def _create_filetag_model(filetag_schema: FileTagCreate = Body(..., description="create schema"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    create filetag model based on create schema, return filetag schema
    - **status=-1**: filetag count exceed limit
    - **status=-2**: filetag name invalid or existed
    """
    user_id = current_user.id
    filter0 = FileTag.user_id == user_id

    # check if filetag count exceed limit
    if session.query(FileTag).filter(filter0).count() >= 1000:
        return RespFileTag(status=-1, msg="filetag count exceed limit")
    filetag_name = filetag_schema.name.strip()

    # check if filetag name is valid
    if (not filetag_name) or (filetag_name in FILETAG_SYSTEM_SET):
        return RespFileTag(status=-2, msg="filetag name invalid or existed")
    filter1 = FileTag.name == filetag_name

    # check if filetag name existed
    if session.query(FileTag).filter(filter0, filter1).first():
        return RespFileTag(status=-2, msg="filetag name invalid or existed")
    filetag_id = get_id_string(f"{user_id}-{filetag_name}")

    # create filetag model based on create schema, type="custom"
    filetag_kwargs = filetag_schema.model_dump(exclude_unset=True)
    filetag_model = FileTag(id=filetag_id, user_id=user_id, **filetag_kwargs)
    session.add(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data_filetag=FileTagSchema(**filetag_model.dict()))


@router.patch("/{filetag_id}", response_model=RespFileTag)
def _update_filetag_model(filetag_id: str = Path(..., description="filetag id"),
                          filetag_schema: FileTagUpdate = Body(..., description="update schema"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    update filetag model based on update schema, return filetag schema
    - **status=-1**: cannot update system filetag
    - **status=-2**: filetag name invalid or existed
    - **status_code=404**: filetag not found
    """
    user_id = current_user.id
    filter0 = FileTag.user_id == user_id

    # check filetag_id and get filetag model
    filetag_model = check_filetag(filetag_id, user_id, session)
    if filetag_model.type == "system":
        return RespFileTag(status=-1, msg="cannot update system filetag")
    filetag_name = filetag_schema.name.strip()

    # check if filetag name is valid
    if (not filetag_name) or (filetag_name in FILETAG_SYSTEM_SET):
        return RespFileTag(status=-2, msg="filetag name invalid or existed")
    filter1 = FileTag.name == filetag_name

    # check if filetag name existed
    if session.query(FileTag).filter(filter0, filter1).first():
        return RespFileTag(status=-2, msg="filetag name invalid or existed")

    # update filetag model based on update schema
    for field in filetag_schema.model_dump(exclude_unset=True):
        # if field == "name": xxxxxxxx
        setattr(filetag_model, field, getattr(filetag_schema, field))
    session.merge(filetag_model)
    session.commit()

    # return filetag schema
    return RespFileTag(data_filetag=FileTagSchema(**filetag_model.dict()))


@router.delete("/{filetag_id}", response_model=Resp)
def _delete_filetag_model(filetag_id: str = Path(..., description="filetag id"),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    delete filetag model by filetag_id
    - **status=-1**: cannot delete system filetag
    - **status=-2**: filetag not empty with files
    - **status_code=404**: filetag not found
    """
    user_id = current_user.id
    filter0 = FileTag.user_id == user_id

    # check filetag_id and get filetag model
    filetag_model = check_filetag(filetag_id, user_id, session)
    if filetag_model.type == "system":
        return RespFileTag(status=-1, msg="cannot delete system filetag")

    # check if filetag not empty with files
    filter1 = FileTagFile.filetag_id == filetag_id
    if session.query(FileTagFile).filter(filter1).count() > 0:
        return RespFileTag(status=-2, msg="filetag not empty with files")

    # delete filetag model by filetag_id
    session.delete(filetag_model)
    session.commit()

    # return result
    return Resp(msg="delete success")
