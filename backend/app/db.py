from sqlmodel import Session, create_engine, SQLModel, select
from app.core.config import settings

from app.models.blog import Blog

# Create a SQLModel engine from the database URL
engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables():
    # 自動起 Table
    SQLModel.metadata.create_all(engine)
    
    # 檢查有無資料，無就塞一條 (Seed Data)
    with Session(engine) as session:
        statement = select(Blog)
        result = session.exec(statement).first()
        if not result:
            welcome_post = Blog(
                title="Welcome to My Portfolio!",
                excerpt="This is your first blog post generated automatically.",
                content="## Hello World\nSuccessfully connected FastAPI and Vue 3!",
                is_published=True,
                tags=["General", "Tech"]
            )
            session.add(welcome_post)
            session.commit()