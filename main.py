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
from core.settings import settings

# logging config
log_format = "%(asctime)s %(levelname)s %(filename)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.WARNING, datefmt=None)

# define description
description = """
- return 0 when success
- return -1, -2, ... when something wrong in server
- return HttpException(401) only when access_token is invalid
- return HttpException(500) only when file size too large or something wrong in client
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
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
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
        "127.0.0.1",
        "127.0.0.1:8000",
    ],
)

# set middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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
async def _headers(request: Request, call_next):
    """
    add some values to response headers
    """
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Duration"] = str(time.time() - start_time)
    response.headers["X-Version"] = str(settings.APP_VERSION)
    response.headers["X-Debug"] = str(settings.DEBUG)
    return response
