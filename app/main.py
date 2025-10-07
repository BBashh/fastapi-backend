from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from .routers import post, user, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine) #this will create the tables in the database which are defined in models.py file


app = FastAPI()


origins = ["*"] #["https://www.google.com", "https://www.youtube.com"] #this is a list of domains that are allowed to make requests to our api. 
                #     '*' means all domains are allowed

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}

