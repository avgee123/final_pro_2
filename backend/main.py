from typing import Annotated
import models
import activity
from database import SessionLocal
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine
import event



app = FastAPI()


app.include_router(activity.router)
app.include_router(event.router)

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


app.mount("/static", StaticFiles(directory="static"), name="static")

