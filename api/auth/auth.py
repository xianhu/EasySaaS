# _*_ coding: utf-8 _*_

"""
auth api
"""

from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()


# response model
class RespAccessToken(Resp):
    access_token: str = "no token"
    token_type: str = "bearer"


# enum of client_id
class ClientID(str, Enum):
    web = "web"
    ios = "ios"
    android = "android"


@router.post("/access-token", response_model=RespAccessToken)
def _get_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                      session: Session = Depends(get_session),
                      rd_conn: Redis = Depends(get_redis)):
    """
    get access_token based on OAuth2PasswordRequestForm, return access_token
    - **username**: value of email or phone, etc.
    - **password**: value of password, plain text
    - **client_id**: value of client_id, web | ios | android
    - **status=-1**: user not found
    - **status=-2**: password incorrect
    - **status=-3**: client_id invalid
    """
    # get username、password from form_data
    username, pwd_plain = form_data.username, form_data.password

    # get user_model
    if username.find("@") > 0:
        user_model = session.query(User).filter(User.email == username).first()
    else:
        user_model = session.query(User).filter(User.phone == username).first()

    # check if user exist or raise exception
    if (not user_model) or (user_model.status != 1):
        return RespAccessToken(status=-1, msg="user not found")
    pwd_hash = user_model.password

    # check if password correct or raise exception
    if not check_password_hash(pwd_plain, pwd_hash):
        return RespAccessToken(status=-2, msg="password incorrect")
    client_id = form_data.client_id or "web"

    # check if client_id valid
    if client_id not in ClientID.__members__:
        return RespAccessToken(status=-3, msg="client_id invalid")
    user_id = user_model.id

    # create access_token based on user_id and client_id
    expire_duration = settings.ACCESS_TOKEN_EXPIRE_DURATION
    access_token = create_jwt_token(user_id, expire_duration=expire_duration, client_id=client_id)

    # save access_token to redis and set expire time
    rd_id = f"{settings.APP_NAME}-access-{client_id}-{user_id}"
    rd_conn.set(rd_id, access_token, ex=settings.REFRESH_TOKEN_EXPIRE_DURATION)

    # return access_token
    return RespAccessToken(access_token=access_token)


@router.post("/access-token-logout", response_model=Resp)
def _logout_access_token(client_id: ClientID = Body(..., embed=True, description="client id"),
                         current_user: User = Depends(get_current_user),
                         rd_conn: Redis = Depends(get_redis)):
    """
    logout access_token based on client_id
    """
    user_id = current_user.id

    # delete access_token from redis
    rd_conn.delete(f"{settings.APP_NAME}-access-{client_id}-{user_id}")

    # return result
    return Resp(msg="logout success")
