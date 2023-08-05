# _*_ coding: utf-8 _*_

"""
auth api
"""

from ..base import *


# response model
class RespSend(Resp):
    token: Optional[str] = Field(None)


# enum of ttype
class TypeName(str, Enum):
    signup = "signup"
    reset = "reset"


# enum of client_id
class ClientID(str, Enum):
    web = "web"
    ios = "ios"
    android = "android"


def init_user_object(user_schema: UserCreate, session: Session) -> User:
    """
    initialize user object based on create schema, return user model
    """
    try:
        # create user model based on create schema
        user_id = get_id_string(f"{user_schema.password}-{time.time()}")
        user_model = User(id=user_id, **user_schema.model_dump(exclude_unset=True))
        session.add(user_model)
        session.flush()  # not commit

        # create filetag models
        for filetag_name in FILETAG_SYSTEM_SET:
            # create filetag_id and filetag schema
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
        session.rollback()
        raise excep
