from fastapi import FastAPI
from ml_model import router

app = FastAPI()
app.include_router(router)