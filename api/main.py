from fastapi import FastAPI

app = FastAPI(title="Secure Medical Notes API (Starter)")

@app.get("/")
def healthcheck():
    return {"status": "ok"}