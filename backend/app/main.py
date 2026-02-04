from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends

from contextlib import asynccontextmanager
from sqlmodel import Session

from app.db import get_session
from app.db import init_db
from app.api.v1.blog import router as blog_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 【開機時執行】
    print("🚀 正在初始化資料庫...")
    init_db() 
    yield
    
    # 【熄機時執行】
    print("👋 正在關閉 API...")
    

app = FastAPI(
    title="Tom's Portfolio API",
    lifespan=lifespan
)

app.include_router(blog_router, prefix="/api/v1/blog")

# Allow which addresses to fetch data from
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, this is the root of the API"}