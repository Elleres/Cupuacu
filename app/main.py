from fastapi import FastAPI

from api.v1.user import router as user_router


app = FastAPI()

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "API FastAPI rodando no Docker com sucesso 🚀"}