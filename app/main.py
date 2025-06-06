from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from api.v1 import router


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()

app.include_router(router)

