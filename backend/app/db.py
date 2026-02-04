from sqlmodel import Session, create_engine, SQLModel
from app.core.config import settings

# Create a SQLModel engine from the database URL
engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session