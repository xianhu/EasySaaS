# _*_ coding: utf-8 _*_

"""
FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from core.settings import settings

# create app
app = FastAPI(title=settings.APP_NAME)

# set middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# set router
app.include_router(api_router, prefix="/api")
