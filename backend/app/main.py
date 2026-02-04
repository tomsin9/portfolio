from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import secrets
from contextlib import asynccontextmanager
from sqlmodel import Session
from app.core.config import settings

from app.db import get_session
from app.db import init_db, create_db_and_tables
from app.api.v1.blog import router as blog_router

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
    # 【開機時執行】
    print("🚀 正在初始化資料庫...")
    # init_db() 
    create_db_and_tables() # 佢已經包含咗 init_db() 嘅功能
    yield
    
    # 【熄機時執行】
    print("👋 正在關閉 API...")
    

app = FastAPI(
    title="Portfolio Website API",
    lifespan=lifespan,
    docs_url="/secret-admin-portal"
)

app.include_router(blog_router, prefix="/api/v1/blog")

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