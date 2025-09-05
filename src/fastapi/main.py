from fastapi import FastAPI, Form
import logging

app = FastAPI()

logging.basicConfig(
    filename='/app/logs/fastapi.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@app.get("/health")
def health():
    return {"status": "alive"}


@app.post("/login")
def login(
    user: str = Form(...),
    password: str = Form(...)
):
    return {"message": f"Welcome {user}"}
