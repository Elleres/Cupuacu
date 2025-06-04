from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from api.v1 import router
app = FastAPI()

app.include_router(router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/teste")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "Hello World"}