# _*_ coding: utf-8 _*_

"""
user api
"""

from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()


@router.post("/send-code", response_model=RespSend)
def _send_code_to_xxxx(background_tasks: BackgroundTasks,
                       username: EmailStr | PhoneStr = Body(..., embed=True, description="email or phone"),
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session),
                       rd_conn: Redis = Depends(get_redis)):
    """
    send a code to email or phone for bind, return token with code
    - **status=-1**: send code too frequently
    - **status=-2**: email or phone existed
    """
    # check if send code too frequently
    if rd_conn.get(f"{settings.APP_NAME}-send-{username}"):
        return RespSend(status=-1, msg="send code too frequently")

    # check if email or phone existed
    if username.find("@") > 0:
        user_model = session.query(User).filter(User.email == username).first()
    else:
        user_model = session.query(User).filter(User.phone == username).first()
    if user_model:
        return RespSend(status=-2, msg="email or phone existed")
    code = random.randint(100000, 999999)

    # define token based on username
    data = dict(code=code, type=current_user.id)
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
                       current_user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """
    verify code & token from send-code, and bind email or phone to user
    - **status=-1**: token invalid or expired
    - **status=-2**: code invalid or not match
    """
    # get payload from token, audience="send"
    payload = get_jwt_payload(token, audience="send")

    # check token: type
    if (not payload) or (not payload.get("type")):
        return Resp(status=-1, msg="token invalid or expired")
    if payload["type"] != current_user.id:
        return Resp(status=-1, msg="token invalid or expired")
    # type = payload["type"]

    # check token: sub(email/phone) and code(int)
    if (not payload.get("sub")) or (not payload.get("code")):
        return Resp(status=-1, msg="token invalid or expired")
    username, code_in_token = payload["sub"], payload["code"]

    # check token: code
    if code != code_in_token:
        return Resp(status=-2, msg="code invalid or not match")

    # update user model based on email or phone
    if username.find("@") > 0:
        current_user.email = username
        current_user.email_verified = True
    else:
        current_user.phone = username
        current_user.phone_verified = True
    session.merge(current_user)
    session.commit()

    # return result
    return Resp(msg="bind success")
