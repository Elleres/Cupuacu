import asyncio
import os

from api.v1 import router
from const.const import ENVIRONMENT, ROOT_PATH_URL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from utils.startup import create_initial_admin_acc

print(ENVIRONMENT == "prod", flush=True)
if ENVIRONMENT == "prod":
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=ROOT_PATH_URL + "/token")
    app = FastAPI(
        swagger_ui_parameters={"docExpansion": "none"}, root_path=ROOT_PATH_URL
    )
else:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
    app = FastAPI(swagger_ui_parameters={"docExpansion": "none"})

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

app.include_router(router)

# Não criar conta adm inicial em ambiente de teste
if os.getenv("ENVIRONMENT") != "test":
    asyncio.create_task(create_initial_admin_acc())
