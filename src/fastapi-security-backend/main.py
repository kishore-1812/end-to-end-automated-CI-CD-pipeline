from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "alive"}

# @app.post("/login")
# def login(user: str = Form(...), password: str = Form(...)):
#     return {"message":f"Welcome {user}"}
