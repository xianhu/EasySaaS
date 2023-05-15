# _*_ coding: utf-8 _*_

"""
api module
"""

from fastapi import APIRouter

from . import auth, files, project, user

# define api_router
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(project.router, prefix="/project", tags=["project"])


@api_router.get("/")
async def root():
    return {"message": "Hello World"}
