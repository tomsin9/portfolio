from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import secrets
from contextlib import asynccontextmanager
from sqlmodel import Session
from app.core.config import settings

from app.db.session import get_session
from app.db.session import init_db, create_db_and_tables
from app.api.v1.api import api_router

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    is_correct_username = secrets.compare_digest(credentials.username, settings.API_ADMIN_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, settings.API_ADMIN_PASSWORD)
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When the server starts
    print("🚀 Initializing database...")
    # init_db() 
    create_db_and_tables() # It already contains the init_db() function
    yield
    
    # When the server stops
    print("👋 Stopping API...")
    

app = FastAPI(
    title="Personal website API",
    lifespan=lifespan,
    docs_url="/admin/414",
    swagger_ui_parameters={"persistAuthorization": True},  # Remember auth in Swagger UI
)

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, this is the root of the API"}