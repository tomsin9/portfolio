from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from app.core.config import settings

from app.api.v1.api import api_router
from app.db.session import get_session
from app.db.session import init_db, create_db_and_tables, engine

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
    docs_url=settings.ADMIN_DOCS_URL,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "defaultModelsExpandDepth": -1
    },  # Remember auth in Swagger UI
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