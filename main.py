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

# create app
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    version="1.0.0-beta" if settings.DEBUG else "1.0.0",
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
async def startup_event():
    """
    startup event
    """
    logging.warning("startup...")
    return None


@app.on_event("shutdown")
async def shutdown_event():
    """
    shutdown event
    """
    logging.warning("shutdown...")
    return None


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    """
    add process time to response header
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
