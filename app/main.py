from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "API FastAPI rodando no Docker com sucesso 🚀"}