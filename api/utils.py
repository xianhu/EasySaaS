# _*_ coding: utf-8 _*_

"""
utility functions
"""

from .base import *

# define OAuth2PasswordBearer
_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


def get_current_user(access_token: str = Depends(_oauth2_bearer),
                     session: Session = Depends(get_session),
                     rd_conn: Redis = Depends(get_redis)) -> User:
    """
    check access_token based on token in redis, return user model
    - **status_code=401**: token invalid or expired
    """
    # get payload from access_token
    exception_unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid or expired",
    )
    payload = get_jwt_payload(access_token)

    # check if user_id exist in payload
    if (not payload) or (not payload.get("sub")):
        raise exception_unauthorized
    user_id, client_id = payload["sub"], payload.get("client_id", "web")

    # get token by user_id and client_id, and check if token match
    rd_token = rd_conn.get(f"{settings.APP_NAME}-access-{client_id}-{user_id}")
    if (not rd_token) or (access_token != rd_token):
        raise exception_unauthorized
    user_model = session.query(User).get(user_id)

    # check if user exist or raise exception
    if (not user_model) or (user_model.status != 1):
        raise exception_unauthorized

    # return user
    return user_model


def get_current_user_admin(user_model: User = Depends(get_current_user)) -> User:
    """
    check if user model is admin, return user model
    - **status_code=401**: token invalid or expired
    - **status_code=403**: permission denied
    """
    if user_model.is_admin:
        return user_model
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="permission denied",
    )


def create_user_object(user_schema: UserCreate, session: Session) -> Optional[User]:
    """
    create user object based on create schema, return user model or None
    """
    try:
        # create user model based on create schema
        user_id = get_id_string(f"{user_schema.password}-{time.time()}")
        user_model = User(id=user_id, **user_schema.model_dump(exclude_unset=True))
        user_model.nickname = user_model.email.split("@")[0] if user_model.email else "Guest"
        session.add(user_model)
        session.flush()  # not commit

        # create filetag models
        for filetag_name in FILETAG_SYSTEM_SET:
            # create filetag_id and create schema
            filetag_id = get_id_string(f"{user_id}-{filetag_name}-{time.time()}")
            filetag_schema = FileTagCreate(name=filetag_name, icon="default", color="default")

            # create filetag model based on create schema, ttype="system"
            filetag_kwargs = filetag_schema.model_dump(exclude_unset=True)
            filetag_model = FileTag(id=filetag_id, user_id=user_id, **filetag_kwargs, ttype="system")
            session.add(filetag_model)

        # commit session
        session.commit()
        return user_model
    except Exception as excep:
        logging.error("create user object error: %s", excep)
        session.rollback()
        return None


def delete_user_object(user_model: User, session: Session) -> bool:
    """
    delete user object based on user model, return True or False
    """
    user_id = user_model.id
    try:
        # delete userproject models related to user
        session.query(UserProject).filter(UserProject.user_id == user_id).delete()

        # delete filetag models and filetagfile models related to user
        for filetag_model in session.query(FileTag).filter(FileTag.user_id == user_id).all():
            session.query(FileTagFile).filter(FileTagFile.filetag_id == filetag_model.id).delete()
            session.delete(filetag_model)

        # delete file models and filetagfile models related to user
        for file_model in session.query(File).filter(File.user_id == user_id).all():
            session.query(FileTagFile).filter(FileTagFile.file_id == file_model.id).delete()
            session.delete(file_model)

        # delete userlog models related to user
        session.query(UserLog).filter(UserLog.user_id == user_id).delete()

        # delete user model
        session.delete(user_model)
        session.commit()
        return True
    except Exception as excep:
        logging.error("delete user object error: %s", excep)
        session.rollback()
        return False


def logging_request(request: Request, user_id: str, path: str, session: Session) -> None:
    """
    logging request information to UserLog table
    """
    # get request information
    host = request.client.host
    ua = request.headers.get("user-agent")
    headers = {key: request.headers.get(key) for key in request.headers.keys()}

    # create userlog model and save to database
    userlog_kwargs = dict(host=host, ua=ua, headers=headers, path=path)
    userlog_model = UserLog(user_id=user_id, **userlog_kwargs)
    session.add(userlog_model)
    session.commit()
    return None
