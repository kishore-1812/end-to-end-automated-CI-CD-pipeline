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


# from fastapi import FastAPI, Form
# import logging
# import os

# app = FastAPI()

# API_SECRET = "SuperSecretPassword123!"  # <-- Hardcoded credential

# logging.basicConfig(
#     filename='/app/logs/fastapi.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# @app.get("/health")
# def health():
#     return {"status": "alive"}

# @app.post("/login")
# def login(user: str = Form(...), password: str = Form(...)):
#     return {"message": f"Welcome {user}"}

# @app.get("/runcmd")
# def run_cmd():
#     os.system("ls -l /")  # <-- External command execution

# @app.get("/echo")
# def echo(q: str):
#     return {"result": q}  # <-- Reflected user input
