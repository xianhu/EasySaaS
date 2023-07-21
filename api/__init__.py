# _*_ coding: utf-8 _*_

"""
api module
-------------------
post -> create
put/id -> update all fields
post/id -> update one field
patch/id -> update of schema
get -> read object list
get/id -> read one object
delete/id -> delete one object
-------------------
"""

from typing import Union

from fastapi import APIRouter, Cookie, Header
from fastapi import Request, Response

from core.settings import settings
from . import auth, file, filetag, project, user

# define api_router
api_router = APIRouter(prefix="")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
api_router.include_router(filetag.router, prefix="/filetag", tags=["filetag"])
api_router.include_router(project.router, prefix="/project", tags=["project"])


@api_router.get("/")
async def _root():
    """
    root router
    """
    if not settings.DEBUG:
        return {"message": "Hello World"}
    return {"message": "visit /docs for more information"}


@api_router.get("/test")
async def _test(request: Request,  # parameter of request
                response: Response,  # parameter of response
                fake_cookie: Union[str, None] = Cookie(default=None),
                user_agent: Union[str, None] = Header(default=None)):
    """
    test router
    """
    if not settings.DEBUG:
        return {"message": "Hello World"}

    # set cookie and headers of response
    response.set_cookie(key="fake-cookie", value="1234567890")
    response.headers["X-Fake-Header"] = "1234567890"
    return {
        "request": {
            "cookies": request.cookies,
            "headers": request.headers,
            "client.host": request.client.host,
            "client.port": request.client.port,
        },
        "fake-cookie": fake_cookie,
        "user_agent": user_agent,
    }
