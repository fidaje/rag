from fastapi import FastAPI
from populate.routes import router

app = FastAPI()

app.include_router(router)

