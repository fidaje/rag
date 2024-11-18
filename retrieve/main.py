from fastapi import FastAPI
from retrieve.routes import router

app = FastAPI()

app.include_router(router)