from fastapi import FastAPI
from backend.api.interview import router

from backend.database import Base, engine
import backend.models

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "AI Interview Coach Backend is running 🚀"
    }


app.include_router(router)

# Create database tables
Base.metadata.create_all(bind=engine)