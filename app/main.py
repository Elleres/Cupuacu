import os
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from api.v1 import router

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

if ENVIRONMENT == "prod":
    ROOT_PATH_URL = os.getenv("ROOT_PATH_URL", "")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=ROOT_PATH_URL + "/token")
    app = FastAPI(
        swagger_ui_parameters={"docExpansion": "none"},
        root_path=ROOT_PATH_URL
    )
else:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
    app = FastAPI(
        swagger_ui_parameters={"docExpansion": "none"}
    )

app.include_router(router)

