from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Successfully connected to the database.")
    except Exception as e:
        print("❌ Failed to connect to the database:", str(e))
        raise e

    yield

    print("🛑 Shutting down app...")


app = FastAPI(lifespan=lifespan)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}
