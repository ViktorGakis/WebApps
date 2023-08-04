from fastapi import FastAPI
from uvicorn import run

from fastapi_app import AppFactory

app: FastAPI = AppFactory()

if __name__ == "__main__":
    run("fastapp:app", reload=True, port=8000)

