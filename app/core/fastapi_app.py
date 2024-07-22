# app/core/fastapi_app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import datarefs, commands

def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(datarefs.router)
    app.include_router(commands.router)

    return app
