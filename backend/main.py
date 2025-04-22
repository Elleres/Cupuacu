from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API FastAPI rodando no Docker com sucesso 🚀"}

@app.get("/ping")
def ping():
    return {"pong": True}
