# _*_ coding: utf-8 _*_

"""
utility functions
"""

from .base import *

# define OAuth2PasswordBearer
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


def get_current_user(access_token: str = Depends(oauth2_bearer),
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
    rd_id = f"{settings.APP_NAME}-access-{client_id}-{user_id}"
    if (not rd_conn.get(rd_id)) or (access_token != rd_conn.get(rd_id)):
        raise exception_unauthorized
    user_model = session.query(User).get(user_id)

    # check if user exist or raise exception
    if (not user_model) or (user_model.status != 1):
        raise exception_unauthorized

    # refresh token expire time
    rd_conn.expire(rd_id, settings.REFRESH_TOKEN_EXPIRE_DURATION)

    # return user
    return user_model


def get_current_user_admin(user_model: User = Depends(get_current_user)) -> User:
    """
    check if user model from 'get_current_user' is admin, return user model
    - **status_code=401**: token invalid or expired
    - **status_code=403**: permission denied
    """
    if not user_model.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="permission denied",
        )
    return user_model


def logging_request(request: Request, user_id: str, path: str, session: Session) -> None:
    """
    logging request information to UserLog table
    """
    # get request information
    host = request.client.host
    ua = request.headers.get("user-agent")
    headers = {key: request.headers.get(key) for key in request.headers.keys()}

    # create userlog model based on request information
    userlog_kwargs = dict(host=host, ua=ua, headers=headers, path=path)
    userlog_model = UserLog(user_id=user_id, **userlog_kwargs)
    session.add(userlog_model)
    session.commit()
    return None
