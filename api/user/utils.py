# _*_ coding: utf-8 _*_

"""
user api
"""

from ..base import *


# response model
class RespUser(Resp):
    data_user: Optional[UserSchema] = Field(None)


# response model
class RespUserList(Resp):
    data_user_list: List[UserSchema] = Field([])


def create_user_object(user_schema: UserCreate, session: Session) -> Optional[User]:
    """
    create user object based on create schema, return user model or None
    """
    try:
        # create user_id based on create schema
        if isinstance(user_schema, UserCreateEmail):
            user_id = get_id_string(user_schema.email)
        elif isinstance(user_schema, UserCreatePhone):
            user_id = get_id_string(user_schema.phone)
        else:
            raise Exception("user schema error")

        # create user model based on create schema
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


def delete_user_object(user_id: str, session: Session) -> bool:
    """
    delete user object by user_id, return True or False
    """
    try:
        # delete userproject models and project models(not need) related to user
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

        # delete user model by user_id
        session.query(User).filter(User.id == user_id).delete()

        # commit session
        session.commit()
        return True
    except Exception as excep:
        logging.error("delete user object error: %s", excep)
        session.rollback()
        return False
