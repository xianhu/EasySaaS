# _*_ coding: utf-8 _*_

"""
test mysql
"""

from core import security
from data import SessionMaker
from data.dmysql import init_db
from data.models import *

# init db
init_db()

with SessionMaker() as session:
    # user info =========================================================================
    email = "admin@easysaas.com"
    pwd_hash = security.get_password_hash("a123456")
    user = User(email=email, password=pwd_hash)
    session.add(user)
    session.commit()

    file_tag = FileTag(name="test", user_id=user.id)
    session.add(file_tag)
    session.commit()

    file = File(full_name="test", location="test")
    session.add(file)
    session.commit()

    file_tag_file = FileTagFile(filetag_id=file_tag.id, file_id=file.id)
    session.add(file_tag_file)
    session.commit()

    print(user.filetags)
    print(file.filetags)
    print(file_tag.files)
    exit()

    user_schema = UserCreate(**dict(email=email, password=pwd_hash))

    # create user -- UserCreatePri
    role_json = {"role": "admin", "scopes": ["user:read", ]}
    user_schema = UserCreatePri(id=100001, role_json=role_json, **user_schema.dict(exclude_unset=True))
    user_model = crud_user.create(session, obj_schema=user_schema)
    logging.warning("create user: %s", user_model.to_dict())
    logging.warning("create user: %s", UserSchema(**user_model.to_dict()))

    # user info =========================================================================
    avatar = "https://www.example.com"
    user_schema = UserUpdate(**dict(name="admin", avatar=avatar))

    # update json: must create a new object
    scopes = user_model.role_json["scopes"]
    scopes.append("user:write")
    role_json = {"role": "member", "scopes": scopes}

    # update user -- UserUpdatePri
    user_schema = UserUpdatePri(email_verified=True, role_json=role_json, **user_schema.dict(exclude_unset=True))
    user_model = crud_user.update(session, obj_model=user_model, obj_schema=user_schema)
    logging.warning("update user: %s", user_model.to_dict())
    logging.warning("update user: %s", UserSchema(**user_model.to_dict()))

    # project info ======================================================================
    user_id = user_model.id
    project_name = "demo project"
    project_schema = ProjectCreate(name=project_name, desc=None)

    # create project -- ProjectCreatePri
    project_schema = ProjectCreatePri(id=100001, user_id=user_id, **project_schema.dict(exclude_unset=True))
    project_model = crud_project.create(session, obj_schema=project_schema)
    logging.warning("create project: %s", project_model.to_dict())
    logging.warning("create project: %s", ProjectSchema(**project_model.to_dict()))

    # project info ======================================================================
    desc = "demo project description"
    project_schema = ProjectUpdate(desc=desc)

    # update project -- ProjectUpdatePri
    project_schema = ProjectUpdatePri(**project_schema.dict(exclude_unset=True))
    project_model = crud_project.update(session, obj_model=project_model, obj_schema=project_schema)
    logging.warning("update project: %s", project_model.to_dict())
    logging.warning("update project: %s", ProjectSchema(**project_model.to_dict()))

    # test relationship =================================================================
    logging.warning("user -> projects: %s", user_model.projects[0].to_dict())
    logging.warning("project -> user: %s", project_model.user.to_dict())

    # test get_multi ====================================================================
    user_model_list = crud_user.get_multi(session, offset=0, limit=100)
    logging.warning("user_model_list: %s", user_model_list)
    project_model_list = crud_project.get_multi(session, offset=0, limit=100)
    logging.warning("project_model_list: %s", project_model_list)

    # test delete =======================================================================
    project_model = crud_project.delete(session, _id=project_model.id)
    logging.warning("delete project: %s\n", project_model.to_dict())
