# _*_ coding: utf-8 _*_

"""
user api: 'me' as {user_id}
"""

from .utils import *
from ..base import *
from ..utils import get_current_user, logging_request

# define router
router = APIRouter()


@router.get("/me", response_model=RespUser)
def _get_user_schema(request: Request,  # parameter of request
                     current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    """
    get current_user schema (logging request information)
    """
    # logging request information
    logging_request(request, current_user.id, session)
    # reset reset_time / points / seconds / space if necessary

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.patch("/me", response_model=RespUser)
def _update_user_model(user_schema: UserUpdate = Body(..., description="update schema"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    update current_user model based on update schema, return user schema
    """
    # update user model based on update schema
    for field in user_schema.model_dump(exclude_unset=True):
        # if field == "password": xxxxxxxx
        setattr(current_user, field, getattr(user_schema, field))
    session.merge(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.post("/me/password", response_model=RespUser)
def _update_user_password(password_old: str = Body(..., description="old password"),
                          password_new: str = Body(..., min_length=6, max_length=20),
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """
    update password of current_user model, return user schema
    - **status=-1**: password_old incorrect
    """
    # check password of user model based on password_old
    if not check_password_hash(password_old, current_user.password):
        return RespUser(status=-1, msg="password_old incorrect")
    pwd_hash = get_password_hash(password_new)

    # update password of user model based on pwd_hash
    current_user.password = pwd_hash
    session.merge(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.post("/me/avatar", response_model=RespUser)
def _update_user_avatar(file: UploadFile = UploadFileClass(..., description="file object"),
                        current_user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    """
    update avatar of current_user model, return user schema
    - **status_code=500**: file type not support
    - **status_code=500**: file size too large
    """
    # check file type or raise exception
    if file.content_type not in ["image/jpeg", "image/png"]:
        logging.error("file type not support: %s", file.content_type)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file type not support"
        )

    # check file size or raise exception
    if file.size > 1024 * 1024 * 1:
        logging.error("file size too large: %s", file.size)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="file size too large"
        )
    prefix = file.filename.split(".")[-1]

    # define fullname and location
    fullname = f"{current_user.id}.{prefix}"
    location = f"{FOLDER_AVATAR}/{fullname}"

    # save file to disk or cloud
    with open(location, "wb") as file_in:
        file_in.write(file.file.read())
    avatar_url = f"{settings.APP_DOMAIN}/{location}"

    # update avatar of user model based on avatar_url
    current_user.avatar = avatar_url
    session.merge(current_user)
    session.commit()

    # return user schema
    return RespUser(data_user=UserSchema(**current_user.dict()))


@router.delete("/me", response_model=Resp)
def _delete_user_model(username: EmailStr | PhoneStr = Body(..., description="email or phone"),
                       password: str = Body(..., min_length=6, max_length=20),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    delete current_user model based on username and password
    - **status=-1**: username or password incorrect
    - **status_code=500**: delete user object error
    """
    # check if username and password match current_user
    if (username not in (current_user.email, current_user.phone)) or \
            (not check_password_hash(password, current_user.password)):
        return Resp(status=-1, msg="username or password incorrect")

    # delete user object or raise exception
    delete_user_object(current_user.id, session)

    # return result
    return Resp(msg="delete success")
