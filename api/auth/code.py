# _*_ coding: utf-8 _*_

"""
auth api
"""

from ..base import *
from ..user.utils import create_user_object

# define router
router = APIRouter()


# enum of type
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


@router.post("/send-code", response_model=RespSend)
def _send_code_to_xxxx(background_tasks: BackgroundTasks,
                       username: EmailStr | PhoneStr = Body(..., description="email or phone"),
                       type: TypeName = Body(..., description="type of send"),
                       session: Session = Depends(get_session),
                       rd_conn: Redis = Depends(get_redis)):
    """
    send a code to email or phone for signup or reset, return token with code
    - **status=-1**: send code too frequently
    - **status=-2**: user existed if type is signup
    - **status=-2**: user not exist if type is reset
    """
    # check if send code too frequently
    if rd_conn.get(f"{settings.APP_NAME}-send-{username}"):
        return RespSend(status=-1, msg="send code too frequently")

    # get user_model
    if username.find("@") > 0:
        user_model = session.query(User).filter(User.email == username).first()
    else:
        user_model = session.query(User).filter(User.phone == username).first()

    # check if user exist or not by type
    if type == TypeName.signup and user_model:
        return RespSend(status=-2, msg="user existed")
    if type == TypeName.reset and (not user_model):
        return RespSend(status=-2, msg="user not exist")
    code = random.randint(100000, 999999)

    # define token based on username
    data = dict(code=code, type=type)
    token = create_jwt_token(username, audience="send", **data)

    # send code in background
    if username.find("@") > 0:
        background_tasks.add_task(send_email_of_code, code, username)
    else:
        background_tasks.add_task(send_phone_of_code, code, username)
    rd_conn.set(f"{settings.APP_NAME}-send-{username}", token, ex=60)

    # return token with code
    return RespSend(token=token)


@router.post("/verify-code", response_model=Resp)
def _verify_code_token(code: int = Body(..., description="code from email or phone"),
                       token: str = Body(..., description="token from send-code"),
                       password: str = Body(..., min_length=6, max_length=20),
                       session: Session = Depends(get_session)):
    """
    verify code & token from send-code, and create user or reset password
    - **status=-1**: token invalid or expired
    - **status=-2**: code invalid or not match
    - **status_code=500**: create user object error
    """
    # get payload from token, audience="send"
    payload = get_jwt_payload(token, audience="send")

    # check token: type
    if (not payload) or (not payload.get("type")):
        return Resp(status=-1, msg="token invalid or expired")
    if payload["type"] not in TypeName.__members__:
        return Resp(status=-1, msg="token invalid or expired")
    type = TypeName(payload["type"])

    # check token: sub(email or phone) and code(int)
    if (not payload.get("sub")) or (not payload.get("code")):
        return Resp(status=-1, msg="token invalid or expired")
    pwd_hash = get_password_hash(password)

    # check token: code
    if code != payload["code"]:
        return Resp(status=-2, msg="code invalid or not match")
    username = payload["sub"]

    # get user_model
    if username.find("@") > 0:
        user_model = session.query(User).filter(User.email == username).first()
    else:
        user_model = session.query(User).filter(User.phone == username).first()

    # check token type: signup
    if type == TypeName.signup and (not user_model):
        # create user schema based on username and pwd_hash
        if username.find("@") > 0:
            user_schema = UserCreateEmail(email=username, email_verified=True, password=pwd_hash)
        else:
            user_schema = UserCreatePhone(phone=username, phone_verified=True, password=pwd_hash)

        # create user object or raise exception
        create_user_object(user_schema, session)

        # return result
        return Resp(msg=f"{type} success")

    # check token type: reset
    if type == TypeName.reset and user_model:
        # reset password of user model based on pwd_hash
        user_model.password = pwd_hash
        session.merge(user_model)
        session.commit()

        # return result
        return Resp(msg=f"{type} success")

    # return -1 (token invalid or expired)
    return Resp(status=-1, msg="token invalid or expired")
