from fastapi import FastAPI
from uvicorn import run

from interface.backend import AppFactory

app: FastAPI = AppFactory()

if __name__ == "__main__":
    run("interface:app", reload=True, port=8000)
