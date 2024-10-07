from fastapi import FastAPI, status, Response, HTTPException
from . import schemas, database
from . import models
from .hashing import Hash
from .database import engine, getDb
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
from passlib.context import CryptContext
from .routers import blog, user

app = FastAPI()
getDb = database.getDb
models.Base.metadata.create_all(engine)

#def getDb():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()


app.include_router(blog.router)
app.include_router(user.router)