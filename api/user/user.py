# _*_ coding: utf-8 _*_

"""
user api
"""

from ..base import *
from ..utils import delete_user_object, get_current_user, logging_request

# define router
router = APIRouter()


# response model
class RespUser(Resp):
    data_user: Optional[UserSchema] = Field(None)


@router.get("/me", response_model=RespUser, response_model_exclude_unset=True)
def _get_user_schema(request: Request,  # parameter of request
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    get current_user schema (logging request information)
    """
    # logging request information
    logging_request(request, current_user.id, "/user/me", session)

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.patch("/me", response_model=RespUser, response_model_exclude_unset=True)
def _update_user_model(user_schema: UserUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    update current_user model based on update schema, return user schema
    """
    # update user model based on update schema
    for field in user_schema.model_dump(exclude_unset=True):
        setattr(current_user, field, getattr(user_schema, field))
    session.merge(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.post("/me/password", response_model=RespUser, response_model_exclude_unset=True)
def _update_user_password(password_old: str = Body(..., description="old password"),
                          password_new: str = Body(..., min_length=6, max_length=20),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    update password of current_user model, return user schema
    - **status=-1**: password_old incorrect
    """
    # check password of user model
    if not check_password_hash(password_old, current_user.password):
        return RespUser(status=-1, msg="password_old incorrect")
    pwd_hash = get_password_hash(password_new)

    # update password of user model based on pwd_hash
    current_user.password = pwd_hash
    session.merge(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.post("/me/avatar", response_model=RespUser, response_model_exclude_unset=True)
def _update_user_avatar(file: UploadFile = UploadFileClass(..., description="file object"),
                        current_user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    """
    update avatar of current_user model, return user schema
    - **status_code=500**: file size too large, file type not support
    """
    # check file size or raise exception
    if file.size > settings.MAX_SIZE_AVATAR:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large"
        )
    filename, filetype = file.filename, file.content_type

    # check file type or raise exception
    if filetype not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file type not support"
        )

    # define fullname and save file
    fullname = f"{current_user.id}-{filename}"
    with open(f"{settings.FOLDER_AVATAR}/{fullname}", "wb") as file_in:
        file_in.write(file.file.read())
    avatar_url = f"{settings.APP_DOMAIN}/{settings.FOLDER_AVATAR}/{fullname}"

    # update avatar of user model based on avatar_url
    current_user.avatar = avatar_url
    session.merge(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.delete("/me", response_model=Resp)
def _delete_user_model(current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    delete current_user model (only in DEBUG mode)
    - **status=-1**: delete current_user model failed
    - **status_code=403**: can not delete user model
    """
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="can not delete user model",
        )

    # delete user model and other models
    if not delete_user_object(current_user, session):
        return Resp(status=-1, msg="delete current_user model failed")

    # return result
    return Resp(msg="delete success")
