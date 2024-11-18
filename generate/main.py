from fastapi import FastAPI
from generate.routes import router

app = FastAPI()

app.include_router(router)