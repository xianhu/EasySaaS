# _*_ coding: utf-8 _*_

"""
FastAPI Application
"""

import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles

from api import api_router
from core import settings

# logging config
log_format = "%(asctime)s %(levelname)s %(filename)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.WARNING, datefmt=None)

# define description
description = """
- return status=0(200) when process work successfully
- return status=1, 2, ...(200) when something wrong in process, return data
- return status=-1, -2, ...(200) when something wrong in process, no data
- return HttpException(401) when access_token is invalid or expired
- return HttpException(403) when permission to access source is denied
- return HttpException(500) Internal Server Error when something wrong in server
"""

# create app
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    description=description,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# set middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://127.0.0.1",
        # "http://127.0.0.1:8000",
        "*",  # allow all origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# set middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        # "127.0.0.1",
        # "127.0.0.1:8000",
        "*",  # allow all hosts
    ],
)

# set middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# mount static files
app.mount("/static", StaticFiles(directory="static"))
# app.mount("/avatar", StaticFiles(directory="static/avatar"))
# app.mount("/others", StaticFiles(directory="static/others"))

# set router
app.include_router(api_router)


@app.on_event("startup")
async def _startup_event():
    """
    startup event
    """
    logging.warning("startup...")
    return None


@app.on_event("shutdown")
async def _shutdown_event():
    """
    shutdown event
    """
    logging.warning("shutdown...")
    return None


@app.middleware("http")
async def _http_headers(request: Request, call_next):
    """
    add some values to response headers
    """
    start_time = time.time()
    response = await call_next(request)
    if settings.DEBUG:
        response.headers["X-Duration"] = str(time.time() - start_time)
        response.headers["X-Version"] = str(settings.APP_VERSION)
        response.headers["X-Debug"] = str(settings.DEBUG)
    return response
