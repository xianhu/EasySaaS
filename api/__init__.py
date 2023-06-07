# _*_ coding: utf-8 _*_

"""
api module
"""

from typing import Union

from fastapi import APIRouter, Cookie, Header
from fastapi import Request, Response

from core.settings import settings
from . import auth, files, project, user

# define api_router
api_router = APIRouter(prefix="")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(files.router, prefix="/files", tags=["files"])


@api_router.get("/")
async def root():
    """
    root router
    """
    if not settings.DEBUG:
        return {"message": "Hello World"}
    return {"message": "visit /docs for more information"}


@api_router.get("/test")
async def test(request: Request,
               response: Response,
               session: Union[str, None] = Cookie(default=None),
               user_agent: Union[str, None] = Header(default=None)):
    """
    test router
    """
    if not settings.DEBUG:
        return {"message": "Hello World"}

    # set cookie and headers of response
    response.set_cookie(key="fake-session", value="1234567890")
    response.headers["X-Fake-Header"] = "1234567890"
    return {
        "request": {
            "cookies": request.cookies,
            "headers": request.headers,
            "client.host": request.client.host,
            "client.port": request.client.port,
        },
        "session": session,
        "user_agent": user_agent,
    }
