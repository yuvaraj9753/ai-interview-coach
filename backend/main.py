from fastapi import FastAPI
from backend.api.interview import router

from backend.database import Base, engine
import backend.models  # Ensure models are imported so that they are registered with SQLAlchemy

app = FastAPI()

app.include_router(router)

# Create database tables
Base.metadata.create_all(bind=engine)